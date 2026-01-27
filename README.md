# Web Scraper Tool

A Python-based web scraping tool for extracting content, links, tables, and metadata from web pages.

## Features

- Fetch and parse HTML pages
- Extract text using CSS selectors
- Extract all links from a page
- Extract HTML tables as structured data
- Extract page metadata (title, description, Open Graph tags)
- Export results to JSON or CSV
- Configurable request delay, timeout, and headers
- CLI interface for quick usage

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Scrape a single URL and print results as JSON:

```bash
python main.py https://example.com
```

Scrape with CSS selectors:

```bash
python main.py https://example.com -s headlines=h2 -s prices=span.price
```

Save output to a file:

```bash
python main.py https://example.com -o output/results.json
python main.py https://example.com -o output/results.csv
```

Scrape multiple URLs with a delay:

```bash
python main.py https://example.com https://example.org --delay 2.0
```

### Python API

```python
from scraper import Scraper

s = Scraper()

# Scrape a page
result = s.scrape("https://example.com")
print(result["metadata"]["title"])
print(result["links"])

# Scrape with selectors
result = s.scrape("https://example.com", selectors={"headings": "h2"})
print(result["headings"])

# Scrape multiple pages
results = s.scrape_multiple(["https://example.com", "https://example.org"])
```

## Running Tests

```bash
python -m pytest tests/
```

## Project Structure

```
├── main.py              # CLI entry point
├── requirements.txt     # Python dependencies
├── scraper/
│   ├── __init__.py
│   ├── config.py        # Default configuration
│   ├── scraper.py       # Core Scraper class
│   └── utils.py         # File output and logging helpers
└── tests/
    └── test_scraper.py  # Unit tests
```
