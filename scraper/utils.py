import csv
import json
import os
import logging

logger = logging.getLogger(__name__)


def save_json(data, filepath):
    """Save data to a JSON file."""
    _ensure_dir(filepath)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info("Saved JSON to %s", filepath)


def save_csv(rows, filepath, fieldnames=None):
    """Save a list of dicts to a CSV file.

    If fieldnames is not provided, keys from the first row are used.
    """
    if not rows:
        logger.warning("No data to save to %s", filepath)
        return

    _ensure_dir(filepath)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    logger.info("Saved CSV to %s", filepath)


def setup_logging(level=logging.INFO):
    """Configure logging for the scraper."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _ensure_dir(filepath):
    """Create parent directories for a file path if they don't exist."""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
