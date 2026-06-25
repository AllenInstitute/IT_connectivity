# IT_connectivity

Data files and analysis code associated with the manuscript:

**Cell-type-specific parallel pathways in the canonical cortical microcircuit**

📄 Preprint:  
https://www.biorxiv.org/content/10.64898/2026.04.23.720412v1

## Data files 
📄 Data files can be accessed in an **open AWS S3 bucket** at:
```
s3://allen-paper-supplements/czhang_preprint_2026/
```
**Test accessibility** with the included script (lists every file, confirms each is
readable, and does a pandas read check):
```bash
pip install boto3            # one-time
python test_data_access.py
```
**Download everything** to the current folder (or a chosen directory):
```bash
python test_data_access.py download.
```
Other ways to fetch the same files:
- **AWS CLI** (no credentials): `aws s3 cp --no-sign-request --recursive s3://allen-paper-supplements/czhang_preprint_2026/ .`
- **HTTPS** (any browser / `curl`): `https://allen-paper-supplements.s3.amazonaws.com/czhang_preprint_2026/<filename>`

