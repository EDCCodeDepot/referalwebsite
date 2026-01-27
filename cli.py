#!/usr/bin/env python3
"""Command-line interface for the screen scraper."""

import argparse
import json
import logging
import sys

from scraper.core import Scraper
from scraper.exporter import to_json, to_csv


def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def load_config(path):
    """Load a JSON config file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_scrape(args):
    """Handle the 'scrape' subcommand."""
    scraper = Scraper(
        base_url=args.url,
        delay=args.delay,
        timeout=args.timeout,
    )

    html = scraper.fetch(args.url)
    if html is None:
        print(f"Error: could not fetch {args.url}", file=sys.stderr)
        sys.exit(1)

    if args.mode == "text":
        data = scraper.extract_text(html, args.selector)
    elif args.mode == "attr":
        if not args.attribute:
            print("Error: --attribute is required for mode 'attr'", file=sys.stderr)
            sys.exit(1)
        data = scraper.extract_attributes(html, args.selector, args.attribute)
    elif args.mode == "table":
        data = scraper.extract_table(html, args.selector)
    elif args.mode == "links":
        data = scraper.find_links(html, pattern=args.pattern)
    elif args.mode == "meta":
        data = scraper.extract_meta(html)
    else:
        print(f"Error: unknown mode '{args.mode}'", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        if args.output.endswith(".csv"):
            if isinstance(data, list):
                to_csv(data, args.output)
            else:
                to_csv([data], args.output)
        else:
            to_json(data, args.output)
        print(f"Output written to {args.output}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_batch(args):
    """Handle the 'batch' subcommand using a config file."""
    config = load_config(args.config)

    urls = config.get("urls", [])
    selector = config.get("selector", "body")
    mode = config.get("mode", "text")
    attribute = config.get("attribute")
    delay = config.get("delay", 1.0)
    timeout = config.get("timeout", 30)

    scraper = Scraper(delay=delay, timeout=timeout)
    extract = "attr" if mode == "attr" else "text"
    results = scraper.scrape_pages(urls, selector, extract=extract, attribute=attribute)

    if args.output:
        to_json(results, args.output)
        print(f"Output written to {args.output}")
    else:
        print(json.dumps(results, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        prog="scraper",
        description="Screen scraping tool — extract data from web pages.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- scrape command ---
    sp_scrape = subparsers.add_parser("scrape", help="Scrape a single URL")
    sp_scrape.add_argument("url", help="URL to scrape")
    sp_scrape.add_argument("-s", "--selector", default="body", help="CSS selector (default: body)")
    sp_scrape.add_argument(
        "-m", "--mode",
        choices=["text", "attr", "table", "links", "meta"],
        default="text",
        help="Extraction mode (default: text)",
    )
    sp_scrape.add_argument("-a", "--attribute", help="HTML attribute to extract (for mode 'attr')")
    sp_scrape.add_argument("-p", "--pattern", help="Link filter pattern (for mode 'links')")
    sp_scrape.add_argument("-o", "--output", help="Output file path (.json or .csv)")
    sp_scrape.add_argument("--delay", type=float, default=1.0, help="Request delay in seconds")
    sp_scrape.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    sp_scrape.set_defaults(func=cmd_scrape)

    # --- batch command ---
    sp_batch = subparsers.add_parser("batch", help="Batch scrape from a config file")
    sp_batch.add_argument("config", help="Path to JSON config file")
    sp_batch.add_argument("-o", "--output", help="Output file path (.json)")
    sp_batch.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    setup_logging(args.verbose)
    args.func(args)


if __name__ == "__main__":
    main()
