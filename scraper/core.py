"""Core scraper module for fetching and extracting web page data."""

import time
import logging
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Scraper:
    """A configurable web scraper that fetches pages and extracts data."""

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    def __init__(self, base_url=None, headers=None, delay=1.0, timeout=30):
        """
        Initialize the scraper.

        Args:
            base_url: Optional base URL for resolving relative links.
            headers: Custom HTTP headers (merged with defaults).
            delay: Seconds to wait between requests.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        if headers:
            self.session.headers.update(headers)

    def fetch(self, url):
        """
        Fetch the raw HTML content of a URL.

        Returns:
            The response text, or None on failure.
        """
        try:
            logger.info("Fetching %s", url)
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            logger.error("Failed to fetch %s: %s", url, exc)
            return None

    def parse(self, html):
        """Parse HTML string into a BeautifulSoup document."""
        return BeautifulSoup(html, "lxml")

    def extract_text(self, html, selector):
        """
        Extract text content from all elements matching a CSS selector.

        Args:
            html: Raw HTML string.
            selector: CSS selector string.

        Returns:
            List of stripped text strings.
        """
        soup = self.parse(html)
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements]

    def extract_attributes(self, html, selector, attribute):
        """
        Extract a specific attribute from all elements matching a CSS selector.

        Args:
            html: Raw HTML string.
            selector: CSS selector string.
            attribute: HTML attribute name to extract (e.g. "href", "src").

        Returns:
            List of attribute values.
        """
        soup = self.parse(html)
        elements = soup.select(selector)
        results = []
        for el in elements:
            value = el.get(attribute)
            if value is not None:
                if attribute in ("href", "src") and self.base_url:
                    value = urljoin(self.base_url, value)
                results.append(value)
        return results

    def extract_table(self, html, selector="table"):
        """
        Extract tabular data from the first table matching the selector.

        Returns:
            List of dicts (one per row) keyed by header text,
            or list of lists if no headers are found.
        """
        soup = self.parse(html)
        table = soup.select_one(selector)
        if not table:
            return []

        headers = [th.get_text(strip=True) for th in table.select("th")]
        rows = []
        for tr in table.select("tr"):
            cells = [td.get_text(strip=True) for td in tr.select("td")]
            if not cells:
                continue
            if headers and len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
            else:
                rows.append(cells)
        return rows

    def extract_meta(self, html):
        """
        Extract common metadata from a page.

        Returns:
            Dict with title, description, and og tags.
        """
        soup = self.parse(html)
        meta = {}
        title_tag = soup.find("title")
        if title_tag:
            meta["title"] = title_tag.get_text(strip=True)

        desc = soup.find("meta", attrs={"name": "description"})
        if desc and desc.get("content"):
            meta["description"] = desc["content"]

        for og in soup.find_all("meta", attrs={"property": lambda x: x and x.startswith("og:")}):
            key = og["property"]
            meta[key] = og.get("content", "")

        return meta

    def scrape_pages(self, urls, selector, extract="text", attribute=None):
        """
        Scrape multiple pages with a consistent selector.

        Args:
            urls: List of URLs to scrape.
            selector: CSS selector to target.
            extract: "text" for text content, "attr" for attribute values.
            attribute: Required when extract="attr".

        Returns:
            Dict mapping URL to extracted data list.
        """
        results = {}
        for i, url in enumerate(urls):
            html = self.fetch(url)
            if html is None:
                results[url] = []
                continue

            if extract == "attr" and attribute:
                results[url] = self.extract_attributes(html, selector, attribute)
            else:
                results[url] = self.extract_text(html, selector)

            if i < len(urls) - 1 and self.delay > 0:
                time.sleep(self.delay)

        return results

    def find_links(self, html, pattern=None):
        """
        Find all links on a page, optionally filtered by a substring pattern.

        Args:
            html: Raw HTML string.
            pattern: Optional substring that href must contain.

        Returns:
            List of absolute URLs.
        """
        links = self.extract_attributes(html, "a[href]", "href")
        if pattern:
            links = [link for link in links if pattern in link]
        return links
