# 6G-XR_UC1_Congestion_Control_QoD Dataset

This repository contains the data and logs generated during the validation of the QoD within the 6G-XR project. The specific test cases as well their results, are described in the deliverable D6.1, available at the 6G-XR web page.

Dataset files for UC1 congestion control using QoD measurements.

## Contents

- [`Dataset files/`](Dataset%20files/) contains the merged CSV exports grouped by metric.
- Raw session CSV inputs are kept in the repository for traceability and are ignored by default for new Git additions.

## Available datasets

- `fps_merged.csv`
- `latency_merged.csv`
- `throughput_interf_high_merged.csv`
- `throughput_interf_low_merged.csv`
- `throughput_xr_user_merged.csv`

## Data format

Each merged CSV includes the following metadata columns before the metric values:

- `session_name`
- `session_id`
- `session_time`
- `metric`
- `source_file`

The `Time` column is stored in the format `dd:MM:yyyy HH:mm:ss`.
