# 6gxr-uc1_congestion_control_qod

Dataset files for UC1 congestion control using QoD measurements.

## Contents

- [`Dataset files/`](Dataset%20files/) contains the merged CSV exports grouped by metric.
- Raw session CSV inputs are kept in the repository for traceability and are ignored by default for new Git additions.

## Available merged datasets

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
