import unittest
from unittest.mock import patch, MagicMock

from scraper.scraper import Scraper


SAMPLE_HTML = """
<html>
<head>
    <title>Test Page</title>
    <meta name="description" content="A test page for scraping">
    <meta property="og:title" content="OG Test Page">
</head>
<body>
    <h1>Welcome</h1>
    <p class="intro">Hello, world!</p>
    <a href="/about">About</a>
    <a href="https://example.com/contact">Contact</a>
    <table>
        <tr><th>Name</th><th>Value</th></tr>
        <tr><td>Alpha</td><td>1</td></tr>
        <tr><td>Beta</td><td>2</td></tr>
    </table>
</body>
</html>
"""


class TestScraperParsing(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()
        self.soup = self.scraper.parse(SAMPLE_HTML, parser="html.parser")

    def test_extract_metadata(self):
        meta = self.scraper.extract_metadata(self.soup)
        self.assertEqual(meta["title"], "Test Page")
        self.assertEqual(meta["description"], "A test page for scraping")
        self.assertEqual(meta["og:title"], "OG Test Page")

    def test_extract_links(self):
        links = self.scraper.extract_links(self.soup, base_url="https://example.com")
        self.assertIn("https://example.com/about", links)
        self.assertIn("https://example.com/contact", links)

    def test_extract_text_full(self):
        text = self.scraper.extract_text(self.soup)
        self.assertIn("Welcome", text)
        self.assertIn("Hello, world!", text)

    def test_extract_text_selector(self):
        texts = self.scraper.extract_text(self.soup, selector="p.intro")
        self.assertEqual(texts, ["Hello, world!"])

    def test_extract_tables(self):
        tables = self.scraper.extract_tables(self.soup)
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0][0], {"Name": "Alpha", "Value": "1"})
        self.assertEqual(tables[0][1], {"Name": "Beta", "Value": "2"})


class TestScraperFetch(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()

    @patch.object(Scraper, "fetch")
    def test_scrape_returns_result(self, mock_fetch):
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.status_code = 200
        mock_fetch.return_value = mock_response

        result = self.scraper.scrape("https://example.com")
        self.assertEqual(result["url"], "https://example.com")
        self.assertEqual(result["status_code"], 200)
        self.assertIn("metadata", result)
        self.assertIn("links", result)

    @patch.object(Scraper, "fetch")
    def test_scrape_returns_none_on_failure(self, mock_fetch):
        mock_fetch.return_value = None
        result = self.scraper.scrape("https://bad-url.example")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
