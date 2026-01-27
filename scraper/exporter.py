"""Export scraped data to CSV or JSON files."""

import csv
import json
import os
import logging

logger = logging.getLogger(__name__)


def ensure_output_dir(path):
    """Create the output directory if it doesn't exist."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def to_json(data, filepath, indent=2):
    """
    Write data to a JSON file.

    Args:
        data: Any JSON-serializable data.
        filepath: Output file path.
        indent: JSON indentation level.
    """
    ensure_output_dir(filepath)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    logger.info("Wrote JSON to %s", filepath)


def to_csv(data, filepath):
    """
    Write a list of dicts to a CSV file.

    Args:
        data: List of dicts with consistent keys.
        filepath: Output file path.
    """
    if not data:
        logger.warning("No data to write to %s", filepath)
        return

    ensure_output_dir(filepath)

    if isinstance(data[0], dict):
        fieldnames = list(data[0].keys())
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    else:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in data:
                if isinstance(row, list):
                    writer.writerow(row)
                else:
                    writer.writerow([row])

    logger.info("Wrote CSV to %s", filepath)
