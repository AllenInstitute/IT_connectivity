# IT_connectivity

This repository contains the analysis notebook **`IT-circuit-Figures-clean.ipynb`** and methods to download the processed data tables used to generate the quantitative figures of the manuscript **Cell-type-specific parallel pathways in the canonical cortical microcircuit**.

📄 **Preprint:**  
https://www.biorxiv.org/content/10.64898/2026.04.23.720412v1

All connectivity/synapse analyses operate on pre-extracted tables from the MICrONS **minnie65_public** dataset (release **v1718**).

## 1. System requirements
### Operating systems
- **Tested on:** Windows 11 (64-bit).
- The code is platform-independent Python and is expected to run unmodified on macOS (≥12) and Linux (e.g. Ubuntu ≥20.04).
### Software dependencies (versions the code was tested on)
Listed in 'requirements.txt'. 

## 2. Installation
This is a standard Jupyter notebook with pip-installable dependencies, so **any** Python environment manager works. The pinned, tested versions are listed in the included `requirements.txt`.

 **(Figure 1 skeleton cell only) Set up a CAVE token** (Skip this step if you do not need to run the Figure 1 skeleton panel) 
 — need to query `minnie65_public` and fetch the example skeleton:
   ```python
   from caveclient import CAVEclient
   client = CAVEclient('minnie65_public')
   client.auth.setup_token(make_new=True)     # opens a browser; copy the token
   client.auth.save_token(token="<YOUR_TOKEN>")
   ```
   (Free registration at https://global.daf-apis.com/auth.) 
### Typical install time
- **~5–20 minutes** on a normal desktop with a broadband connection.

## 3. Data files 
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
**Unzip the input-synapse table**:
   - Extract `All-E-input-synapses-v1718.zip` → `All-E-input-synapses-v1718.parquet` into the same data folder.

## 4. Demo and instructions for use
The provided data files **are** the demo dataset — the notebook reproduces the manuscript figures directly from them.
### Instructions
   In the **third code cell**, set the `path` variable to the folder that contains the downloaded data files, e.g.:
   ```python
   path = r"C:/Users/<you>/.../Data/"   # Windows
   path = "/home/<you>/.../Data/"     # macOS/Linux
   ```
   Run specific cells to generate associated figures.
### Expected output
- Each figure section renders its panel(s) **inline** in the notebook
### Expected run time
 - **<1 minute** for each panel

### (Optional) Recomputing the Figure 3 spatial shuffle
The per-cell shuffle inputs are provided separately as **`spatial shuffle.zip`** (≈188 MB) in the S3 bucket. It unzips to a folder `spatial shuffle/` containing **114 files** named`<Nucleus_ID>_spatial_shuffle_ids.csv` — one per proofread neuron. Each row is a real synapse paired with one spatially-permitted shuffle target (key columns: `real_synapse_id`, `real_post_nuc_id`, `shuffled_post_nuc_id`, `shuffled_synapse_id`).
