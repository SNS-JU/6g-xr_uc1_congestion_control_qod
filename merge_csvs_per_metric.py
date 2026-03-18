#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


FILE_PATTERN = re.compile(
    r"^(?P<session_name>Demo_Session_(?P<session_id>\d+)_(?P<session_time>\d+_\d+))_(?P<metric>.+)\.csv$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge session CSV files into one CSV per metric."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the source CSV files. Defaults to the current directory.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for merged CSV files. Defaults to <input-dir>/merged_by_metric.",
    )
    parser.add_argument(
        "--pattern",
        default="*.csv",
        help="Glob pattern used to select source CSV files. Defaults to *.csv.",
    )
    return parser.parse_args()


def discover_files(input_dir: Path, pattern: str) -> dict[str, list[tuple[dict[str, str], Path]]]:
    grouped_files: dict[str, list[tuple[dict[str, str], Path]]] = defaultdict(list)

    for path in sorted(input_dir.glob(pattern)):
        if not path.is_file():
            continue

        match = FILE_PATTERN.match(path.name)
        if not match:
            continue

        info = match.groupdict()
        grouped_files[info["metric"]].append((info, path))

    return grouped_files


def format_timestamp(value: str) -> str:
    try:
        timestamp_ms = int(value)
    except (TypeError, ValueError):
        return value

    dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    return dt.strftime("%d:%m:%Y %H:%M:%S")


def merge_metric(metric: str, entries: list[tuple[dict[str, str], Path]], output_dir: Path) -> Path:
    if not entries:
        raise ValueError(f"No files found for metric '{metric}'.")

    output_path = output_dir / f"{metric}_merged.csv"
    output_dir.mkdir(parents=True, exist_ok=True)

    base_headers: list[str] | None = None

    with output_path.open("w", newline="", encoding="utf-8") as merged_file:
        writer: csv.DictWriter | None = None

        for info, path in sorted(
            entries,
            key=lambda item: (
                int(item[0]["session_id"]),
                item[0]["session_time"],
                item[1].name,
            ),
        ):
            with path.open("r", newline="", encoding="utf-8-sig") as source_file:
                reader = csv.DictReader(source_file)

                if reader.fieldnames is None:
                    raise ValueError(f"CSV file '{path}' is missing a header row.")

                if base_headers is None:
                    base_headers = reader.fieldnames
                    merged_headers = [
                        "session_name",
                        "session_id",
                        "session_time",
                        "metric",
                        "source_file",
                        *base_headers,
                    ]
                    writer = csv.DictWriter(merged_file, fieldnames=merged_headers)
                    writer.writeheader()
                elif reader.fieldnames != base_headers:
                    raise ValueError(
                        f"Header mismatch for metric '{metric}' in '{path.name}'. "
                        f"Expected {base_headers}, found {reader.fieldnames}."
                    )

                assert writer is not None

                for row in reader:
                    if "Time" in row:
                        row["Time"] = format_timestamp(row["Time"])

                    merged_row = {
                        "session_name": info["session_name"],
                        "session_id": info["session_id"],
                        "session_time": info["session_time"],
                        "metric": metric,
                        "source_file": path.name,
                    }
                    merged_row.update(row)
                    writer.writerow(merged_row)

    return output_path


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir / "merged_by_metric").resolve()

    grouped_files = discover_files(input_dir, args.pattern)
    if not grouped_files:
        raise SystemExit(
            f"No matching session CSV files found in '{input_dir}' using pattern '{args.pattern}'."
        )

    created_files = []
    for metric, entries in sorted(grouped_files.items()):
        created_files.append(merge_metric(metric, entries, output_dir))

    print(f"Created {len(created_files)} merged files in {output_dir}:")
    for path in created_files:
        print(f" - {path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
