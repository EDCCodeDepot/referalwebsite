# Screen Scraper

A Python command-line tool for extracting data from web pages using CSS selectors. Supports text extraction, attribute extraction, table parsing, link discovery, and metadata collection. Export results to JSON or CSV.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Scrape a single page

Extract text from elements matching a CSS selector:

```bash
python cli.py scrape https://example.com -s "h1"
```

Extract `href` attributes from all links:

```bash
python cli.py scrape https://example.com -m attr -s "a" -a href
```

Extract a table:

```bash
python cli.py scrape https://example.com/data -m table -s "table.results"
```

Find all links containing a pattern:

```bash
python cli.py scrape https://example.com -m links -p "/product/"
```

Get page metadata (title, description, Open Graph tags):

```bash
python cli.py scrape https://example.com -m meta
```

### Save output to a file

```bash
python cli.py scrape https://example.com -s "h2" -o output/results.json
python cli.py scrape https://example.com -m table -o output/data.csv
```

### Batch scrape from a config file

```bash
python cli.py batch config.example.json -o output/batch.json
```

See `config.example.json` for the config format.

### Options

| Flag | Description |
|------|-------------|
| `-s, --selector` | CSS selector (default: `body`) |
| `-m, --mode` | Extraction mode: `text`, `attr`, `table`, `links`, `meta` |
| `-a, --attribute` | HTML attribute to extract (for `attr` mode) |
| `-p, --pattern` | Substring filter for links (for `links` mode) |
| `-o, --output` | Output file (`.json` or `.csv`) |
| `--delay` | Delay between requests in seconds (default: 1.0) |
| `--timeout` | Request timeout in seconds (default: 30) |
| `-v, --verbose` | Enable debug logging |

## Using as a library

```python
from scraper import Scraper

s = Scraper(base_url="https://example.com", delay=0.5)
html = s.fetch("https://example.com")

titles = s.extract_text(html, "h2.title")
links = s.find_links(html, pattern="/article/")
meta = s.extract_meta(html)
table = s.extract_table(html, "table#stats")
```

## Project structure

```
├── cli.py                 # Command-line interface
├── scraper/
│   ├── __init__.py
│   ├── core.py            # Scraper class (fetch, parse, extract)
│   └── exporter.py        # JSON and CSV export
├── config.example.json    # Example batch config
├── requirements.txt
└── README.md
```
