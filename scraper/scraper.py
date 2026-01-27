import time
import logging
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from scraper.config import DEFAULT_HEADERS, DEFAULT_TIMEOUT, DEFAULT_DELAY

logger = logging.getLogger(__name__)


class Scraper:
    """A general-purpose web scraper that extracts content from web pages."""

    def __init__(self, headers=None, timeout=None, delay=None):
        self.session = requests.Session()
        self.session.headers.update(headers or DEFAULT_HEADERS)
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.delay = delay or DEFAULT_DELAY

    def fetch(self, url):
        """Fetch raw HTML content from a URL.

        Returns the Response object or None on failure.
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error("Failed to fetch %s: %s", url, e)
            return None

    def parse(self, html, parser="lxml"):
        """Parse HTML content into a BeautifulSoup object."""
        return BeautifulSoup(html, parser)

    def extract_links(self, soup, base_url=None):
        """Extract all links from a parsed page.

        Returns a list of absolute URLs.
        """
        links = []
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if base_url:
                href = urljoin(base_url, href)
            links.append(href)
        return links

    def extract_text(self, soup, selector=None):
        """Extract text content from a parsed page.

        If a CSS selector is provided, only text within matching elements is
        returned. Otherwise, the full page text is returned.
        """
        if selector:
            elements = soup.select(selector)
            return [el.get_text(strip=True) for el in elements]
        return soup.get_text(strip=True)

    def extract_tables(self, soup):
        """Extract all HTML tables as lists of row-dicts.

        Each table is returned as a list of dictionaries keyed by header text.
        """
        tables = []
        for table in soup.find_all("table"):
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cells:
                    if headers and len(cells) == len(headers):
                        rows.append(dict(zip(headers, cells)))
                    else:
                        rows.append(cells)
            tables.append(rows)
        return tables

    def extract_metadata(self, soup):
        """Extract page metadata (title, description, og tags)."""
        meta = {}
        title_tag = soup.find("title")
        if title_tag:
            meta["title"] = title_tag.get_text(strip=True)

        desc_tag = soup.find("meta", attrs={"name": "description"})
        if desc_tag and desc_tag.get("content"):
            meta["description"] = desc_tag["content"]

        for tag in soup.find_all("meta", attrs={"property": True}):
            prop = tag.get("property", "")
            if prop.startswith("og:") and tag.get("content"):
                meta[prop] = tag["content"]

        return meta

    def scrape(self, url, selectors=None):
        """High-level method: fetch, parse, and extract data from a URL.

        Args:
            url: The page URL to scrape.
            selectors: Optional dict mapping field names to CSS selectors.
                       e.g. {"headlines": "h2.title", "prices": "span.price"}

        Returns:
            A dict with metadata, links, and extracted fields (or full text).
        """
        response = self.fetch(url)
        if response is None:
            return None

        soup = self.parse(response.text)
        result = {
            "url": url,
            "status_code": response.status_code,
            "metadata": self.extract_metadata(soup),
            "links": self.extract_links(soup, base_url=url),
        }

        if selectors:
            for name, selector in selectors.items():
                result[name] = self.extract_text(soup, selector)
        else:
            result["text"] = self.extract_text(soup)

        return result

    def scrape_multiple(self, urls, selectors=None):
        """Scrape a list of URLs with a delay between requests.

        Returns a list of result dicts.
        """
        results = []
        for i, url in enumerate(urls):
            logger.info("Scraping %d/%d: %s", i + 1, len(urls), url)
            result = self.scrape(url, selectors=selectors)
            if result:
                results.append(result)
            if i < len(urls) - 1:
                time.sleep(self.delay)
        return results
