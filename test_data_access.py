"""Test accessibility of the manuscript data files on the open S3 bucket.

    s3://allen-paper-supplements/czhang_preprint_2026/

The bucket is PUBLIC, so no AWS account or credentials are needed -- access is
anonymous (unsigned). This script:
  1. lists every object under the prefix,
  2. confirms each EXPECTED file is present and matches by name,
  3. does a tiny ranged read on each to confirm the bytes are actually readable,
  4. (optional) reads one small table with pandas as an end-to-end check,
  5. (optional) downloads all files locally.

Requires:  boto3   (pip install boto3)        # standard for S3
Optional :  pandas, pyarrow                    # for the pandas read test

Run:        python test_data_access.py
"""
import io
import sys
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import ClientError, EndpointConnectionError

BUCKET = "allen-paper-supplements"
PREFIX = "czhang_preprint_2026/"

# Files the analysis notebook expects (unzip the .zip files after download).
EXPECTED = [
    "All-E-input-synapses-v1718.zip",
    "All-E-output-synapses-v1718.parquet",
    "Column-E-output-synapses-v1718.parquet",
    "Column-L23-input-synapse-number-v1718.csv",
    "Column-all-output-v1718-mtype.parquet",
    "Column_mtype_v1718.csv",
    "L5IT-L23-synapse-percentage.csv",
    "L5_IT_lda_umap_features.csv",
    "Proofread IT and ET with root id-v1718.csv",
    "Proofread-V1-output-synapses-with-motif-v1718.csv",
    "Proofread-V1-output-synapses-with-mtypes-v1718.parquet",
    "Proofread_L4_output_synapses_v1718.parquet",
    "V1_mtype_v1718.parquet",
    "V1_prf_inh_connections_v1718.parquet",
    "co_target_mean_all_E_target_v1718.csv",
    "co_target_mean_column_E_target_v1718.csv",
    "prf-LGN-output-mtype-v1718.csv",
    "prf-inh-motif-sorted-v1664.csv",
    "spatial_shuffle_ratio_v1718.csv",
    "synapse_identification_stat_v1718.csv",
]


def human(n):
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{int(n)} B" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{n} B"


def make_client():
    # anonymous / unsigned access -- no AWS credentials required for a public bucket
    return boto3.client("s3", config=Config(signature_version=UNSIGNED))


def list_objects(s3):
    keys = {}
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for o in page.get("Contents", []):
            if o["Key"].endswith("/"):
                continue
            keys[o["Key"][len(PREFIX):]] = o["Size"]
    return keys


def read_check(s3, key):
    """Read the first 1 KB to confirm the object is actually downloadable."""
    try:
        r = s3.get_object(Bucket=BUCKET, Key=PREFIX + key, Range="bytes=0-1023")
        return len(r["Body"].read()) > 0
    except ClientError as e:
        return False


def main():
    print(f"Testing s3://{BUCKET}/{PREFIX}  (anonymous access)\n")
    s3 = make_client()
    try:
        present = list_objects(s3)
    except EndpointConnectionError:
        sys.exit("FAILED: cannot reach S3 endpoint. Check your internet connection.")
    except ClientError as e:
        sys.exit(f"FAILED to list bucket: {e}")

    print(f"Found {len(present)} files under the prefix.\n")
    print(f"{'status':<8}{'read':<6}{'size':>12}  file")
    print("-" * 78)
    ok = miss = 0
    for f in EXPECTED:
        if f in present:
            readable = read_check(s3, f)
            ok += 1
            print(f"{'OK':<8}{('yes' if readable else 'NO!'):<6}{human(present[f]):>12}  {f}")
        else:
            miss += 1
            print(f"{'MISSING':<8}{'-':<6}{'-':>12}  {f}")

    extra = sorted(set(present) - set(EXPECTED))
    if extra:
        print("\nAdditional files in the bucket (not required by the notebook):")
        for f in extra:
            print(f"        {'':6}{human(present[f]):>12}  {f}")

    print("\n" + "=" * 50)
    print(f"accessible: {ok}/{len(EXPECTED)} expected files   missing: {miss}")

    # End-to-end pandas read test on one small table (optional)
    try:
        import pandas as pd
        small = "synapse_identification_stat_v1718.csv"
        if small in present:
            body = s3.get_object(Bucket=BUCKET, Key=PREFIX + small)["Body"].read()
            df = pd.read_csv(io.BytesIO(body))
            print(f"pandas read test: {small} -> {df.shape[0]} rows x {df.shape[1]} cols  [OK]")
    except ImportError:
        print("pandas not installed -> skipped the read-into-DataFrame test.")
    except Exception as e:
        print(f"pandas read test FAILED: {e}")

    print("=" * 50)
    sys.exit(0 if miss == 0 else 1)


def download_all(dest="."):
    """Optional helper: download every file in the prefix to `dest`."""
    import os
    s3 = make_client()
    os.makedirs(dest, exist_ok=True)
    for key, size in list_objects(s3).items():
        out = os.path.join(dest, key)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        print(f"downloading {key} ({human(size)}) ...")
        s3.download_file(BUCKET, PREFIX + key, out)
    print("done.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "download":
        download_all(sys.argv[2] if len(sys.argv) > 2 else ".")
    else:
        main()
