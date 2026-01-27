"""CLI entry point for the web scraper."""

import argparse
import json
import sys

from scraper.scraper import Scraper
from scraper.utils import save_json, save_csv, setup_logging


def main():
    parser = argparse.ArgumentParser(description="Web Scraper Tool")
    parser.add_argument("url", nargs="+", help="URL(s) to scrape")
    parser.add_argument(
        "-s", "--selector",
        action="append",
        metavar="NAME=SELECTOR",
        help="CSS selector for extraction, e.g. -s titles=h2.title",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (.json or .csv)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between requests (default: 1.0)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    import logging
    setup_logging(level=logging.DEBUG if args.verbose else logging.INFO)

    selectors = None
    if args.selector:
        selectors = {}
        for s in args.selector:
            if "=" not in s:
                print(f"Invalid selector format: {s!r} (expected NAME=SELECTOR)", file=sys.stderr)
                sys.exit(1)
            name, sel = s.split("=", 1)
            selectors[name] = sel

    scraper = Scraper(timeout=args.timeout, delay=args.delay)

    if len(args.url) == 1:
        results = scraper.scrape(args.url[0], selectors=selectors)
    else:
        results = scraper.scrape_multiple(args.url, selectors=selectors)

    if results is None:
        print("Scraping failed.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        if args.output.endswith(".csv"):
            data = results if isinstance(results, list) else [results]
            flat = []
            for item in data:
                flat.append({
                    "url": item.get("url", ""),
                    "status_code": item.get("status_code", ""),
                    "title": item.get("metadata", {}).get("title", ""),
                })
            save_csv(flat, args.output)
        else:
            save_json(results, args.output)
    else:
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
