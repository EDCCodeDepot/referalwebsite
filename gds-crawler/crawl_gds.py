#!/usr/bin/env python3
"""
Web crawler for Georgetown Day School (gds.org) - consolidates website into a single readable file.
Designed to run in Claude Code environment.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from collections import deque
from datetime import datetime
import re
import random
from urllib.robotparser import RobotFileParser

class GDSCrawler:
    def __init__(self, base_url="https://www.gds.org", delay=1.5, max_pages=500):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.base_delay = delay
        self.delay = delay
        self.max_pages = max_pages
        self.visited = set()
        self.pages = []
        self.failed_pages = []  # Track failed URLs for retry
        self.session = requests.Session()

        # Realistic browser headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })

        # Retry settings
        self.max_retries = 3
        self.retry_delay = 5

        # Robots.txt parser
        self.robots_parser = None
        self._load_robots_txt()

    def _load_robots_txt(self):
        """Load and parse robots.txt."""
        try:
            robots_url = f"{self.base_url}/robots.txt"
            self.robots_parser = RobotFileParser()
            self.robots_parser.set_url(robots_url)
            self.robots_parser.read()
            print(f"✓ Loaded robots.txt from {robots_url}")

            # Check for crawl-delay directive
            response = self.session.get(robots_url, timeout=10)
            if response.ok:
                for line in response.text.split('\n'):
                    if 'crawl-delay' in line.lower():
                        try:
                            delay = float(line.split(':')[1].strip())
                            if delay > self.delay:
                                self.delay = delay
                                print(f"  → Respecting crawl-delay: {delay}s")
                        except:
                            pass
        except Exception as e:
            print(f"⚠ Could not load robots.txt: {e}")
            print("  → Proceeding with default polite crawling")
            self.robots_parser = None

    def is_allowed_by_robots(self, url):
        """Check if URL is allowed by robots.txt."""
        if self.robots_parser is None:
            return True
        try:
            return self.robots_parser.can_fetch('*', url)
        except:
            return True

    def is_valid_url(self, url):
        """Check if URL belongs to gds.org domain."""
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == f"www.{self.domain}"

    def normalize_url(self, url):
        """Normalize URL to avoid duplicates."""
        parsed = urlparse(url)
        # Remove fragment and trailing slash
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized

    def extract_text(self, soup):
        """Extract readable text from HTML, removing scripts/styles."""
        # Remove non-content elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript']):
            element.decompose()

        # Get text
        text = soup.get_text(separator='\n', strip=True)
        # Clean up excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def extract_links(self, soup, current_url):
        """Extract all valid internal links from page."""
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Convert relative URLs to absolute
            full_url = urljoin(current_url, href)
            normalized = self.normalize_url(full_url)

            # Only include internal links, skip files
            if self.is_valid_url(normalized):
                # Skip common non-HTML resources
                skip_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg',
                                   '.css', '.js', '.zip', '.doc', '.docx', '.xls', '.xlsx')
                if not any(normalized.lower().endswith(ext) for ext in skip_extensions):
                    links.add(normalized)
        return links

    def crawl_page(self, url):
        """Crawl a single page with retry logic and rate limit handling.
        Returns: (page_data, links, failure_reason) - failure_reason is None on success
        """

        # Check robots.txt
        if not self.is_allowed_by_robots(url):
            print(f"         ⊘ Blocked by robots.txt")
            return None, set(), "blocked_by_robots"

        for attempt in range(self.max_retries):
            try:
                # Add slight randomization to appear more human
                time.sleep(random.uniform(0.1, 0.5))

                # Set referer to look like natural browsing
                self.session.headers['Referer'] = self.base_url

                response = self.session.get(url, timeout=30)

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', self.retry_delay * (attempt + 1)))
                    print(f"         ⏳ Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue

                # Handle temporary server errors
                if response.status_code in [500, 502, 503, 504]:
                    wait_time = self.retry_delay * (attempt + 1)
                    print(f"         ⏳ Server error {response.status_code}. Retry in {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                # Handle forbidden/not found
                if response.status_code == 403:
                    print(f"         ⊘ Access forbidden (403)")
                    return None, set(), "forbidden_403"

                if response.status_code == 404:
                    return None, set(), "not_found_404"

                response.raise_for_status()

                # Only process HTML content
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type:
                    return None, set(), "not_html"

                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract title
                title = soup.title.string if soup.title else url

                # Extract main content
                main_content = soup.find('main') or soup.find('article') or soup.find('div', {'role': 'main'})
                if main_content:
                    text = self.extract_text(main_content)
                else:
                    text = self.extract_text(soup)

                # Extract links
                links = self.extract_links(soup, url)

                page_data = {
                    'url': url,
                    'title': title.strip() if title else url,
                    'content': text
                }

                return page_data, links, None  # Success

            except requests.exceptions.Timeout:
                wait_time = self.retry_delay * (attempt + 1)
                print(f"         ⏳ Timeout. Retry {attempt + 1}/{self.max_retries} in {wait_time}s...")
                time.sleep(wait_time)

            except requests.exceptions.ConnectionError:
                wait_time = self.retry_delay * (attempt + 1)
                print(f"         ⏳ Connection error. Retry {attempt + 1}/{self.max_retries} in {wait_time}s...")
                time.sleep(wait_time)

            except Exception as e:
                print(f"         ✗ Error: {e}")
                return None, set(), f"exception: {str(e)}"

        print(f"         ✗ Failed after {self.max_retries} retries")
        return None, set(), "max_retries_exceeded"

    def crawl(self):
        """Crawl the entire website using BFS."""
        queue = deque([self.base_url])
        self.visited.add(self.normalize_url(self.base_url))
        start_time = time.time()
        errors = 0

        print("=" * 60)
        print(f"  GEORGETOWN DAY SCHOOL WEB CRAWLER")
        print("=" * 60)
        print(f"  Target:     {self.base_url}")
        print(f"  Max pages:  {self.max_pages}")
        print(f"  Delay:      {self.delay}s between requests")
        print(f"  Started:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()

        while queue and len(self.pages) < self.max_pages:
            url = queue.popleft()

            # Skip if blocked by robots.txt
            if not self.is_allowed_by_robots(url):
                print(f"  Skipping (robots.txt): {url[:50]}...")
                continue

            elapsed = time.time() - start_time
            pages_collected = len(self.pages)

            # Calculate progress stats
            rate = pages_collected / elapsed if elapsed > 0 else 0
            remaining_estimate = (self.max_pages - pages_collected) / rate / 60 if rate > 0 else 0

            # Status line
            print(f"[{pages_collected + 1:3d}/{self.max_pages}] ", end="")
            print(f"Queue: {len(queue):4d} | ", end="")
            print(f"Errors: {errors:2d} | ", end="")
            print(f"Time: {elapsed/60:.1f}m | ", end="")
            print(f"ETA: {remaining_estimate:.1f}m")
            print(f"         → {url[:70]}{'...' if len(url) > 70 else ''}")

            page_data, links, failure_reason = self.crawl_page(url)

            if page_data and page_data['content']:
                self.pages.append(page_data)
                new_links = 0

                # Add new links to queue
                for link in links:
                    normalized_link = self.normalize_url(link)
                    if normalized_link not in self.visited:
                        self.visited.add(normalized_link)
                        queue.append(link)
                        new_links += 1

                print(f"         ✓ Collected ({len(page_data['content']):,} chars, +{new_links} new links)")
            else:
                errors += 1
                # Track failure for potential retry
                if failure_reason and failure_reason not in ["not_found_404", "not_html", "blocked_by_robots"]:
                    self.failed_pages.append({
                        'url': url,
                        'reason': failure_reason,
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"         ✗ Failed: {failure_reason} (logged for retry)")
                else:
                    print(f"         ✗ Skipped: {failure_reason or 'no content'}")

            print()

            # Randomized polite delay (looks more human)
            actual_delay = self.delay + random.uniform(0.5, 1.5)
            time.sleep(actual_delay)

        # Final summary
        total_time = time.time() - start_time
        total_chars = sum(len(p['content']) for p in self.pages)

        print("=" * 60)
        print("  CRAWL COMPLETE")
        print("=" * 60)
        print(f"  Pages collected:  {len(self.pages)}")
        print(f"  Total characters: {total_chars:,}")
        print(f"  URLs visited:     {len(self.visited)}")
        print(f"  Errors/skipped:   {errors}")
        print(f"  Failed (retry):   {len(self.failed_pages)}")
        print(f"  Total time:       {total_time/60:.1f} minutes")
        print(f"  Avg rate:         {len(self.pages)/total_time:.2f} pages/sec")
        print("=" * 60)

        if self.failed_pages:
            print(f"\n⚠ {len(self.failed_pages)} pages failed and can be retried.")
            print("  See 'gds_failed_pages.json' for details.")

        print()

        return self.pages

    def export_markdown(self, output_path="gds_org_consolidated.md"):
        """Export all crawled content to a single markdown file optimized for LLM reading."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Georgetown Day School - Complete Website Content\n\n")
            f.write(f"Crawled: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Pages: {len(self.pages)}\n\n")
            f.write("=" * 80 + "\n\n")

            # Content - simple format for LLM parsing
            for i, page in enumerate(self.pages, 1):
                f.write(f"PAGE {i}: {page['title']}\n")
                f.write(f"URL: {page['url']}\n")
                f.write("-" * 40 + "\n")
                f.write(page['content'])
                f.write("\n\n" + "=" * 80 + "\n\n")

        print(f"Exported to: {output_path}")
        return output_path

    def export_json(self, output_path="gds_org_consolidated.json"):
        """Export all crawled content to JSON."""
        data = {
            'metadata': {
                'source': self.base_url,
                'crawled_at': datetime.now().isoformat(),
                'total_pages': len(self.pages)
            },
            'pages': self.pages
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Exported to: {output_path}")
        return output_path

    def export_failed_pages(self, output_path="gds_failed_pages.json"):
        """Export failed pages for retry."""
        if not self.failed_pages:
            return None

        data = {
            'metadata': {
                'source': self.base_url,
                'crawled_at': datetime.now().isoformat(),
                'total_failed': len(self.failed_pages)
            },
            'failed_pages': self.failed_pages
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Failed pages logged to: {output_path}")
        return output_path

    def retry_failed_pages(self, failed_json_path="gds_failed_pages.json"):
        """Retry crawling pages from a failed pages JSON file."""
        try:
            with open(failed_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            failed_urls = [p['url'] for p in data.get('failed_pages', [])]
            print(f"\nRetrying {len(failed_urls)} failed pages...")
            print("=" * 60)

            newly_failed = []

            for i, url in enumerate(failed_urls, 1):
                print(f"[Retry {i}/{len(failed_urls)}] {url[:60]}...")

                page_data, links, failure_reason = self.crawl_page(url)

                if page_data and page_data['content']:
                    self.pages.append(page_data)
                    print(f"         ✓ Success! ({len(page_data['content']):,} chars)")
                else:
                    newly_failed.append({
                        'url': url,
                        'reason': failure_reason,
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"         ✗ Still failing: {failure_reason}")

                # Polite delay
                time.sleep(self.delay + random.uniform(0.5, 1.5))

            # Update failed pages list
            self.failed_pages = newly_failed

            print("=" * 60)
            print(f"Retry complete: {len(failed_urls) - len(newly_failed)} recovered, {len(newly_failed)} still failing")

            return len(failed_urls) - len(newly_failed)

        except FileNotFoundError:
            print(f"No failed pages file found at {failed_json_path}")
            return 0

    def _slugify(self, text):
        """Create URL-friendly slug from text."""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        return text[:50]


def main():
    import sys

    # Configuration for Georgetown Day School
    crawler = GDSCrawler(
        base_url="https://www.gds.org",
        delay=1.5,      # 1.5 seconds between requests (be polite)
        max_pages=500   # Adjust as needed
    )

    # Check for retry mode
    if len(sys.argv) > 1 and sys.argv[1] == '--retry':
        print("Running in RETRY mode...")
        crawler.retry_failed_pages("gds_failed_pages.json")

        # Re-export with recovered pages
        if crawler.pages:
            # Load existing data and merge
            try:
                with open("gds_org_consolidated.json", 'r') as f:
                    existing = json.load(f)
                existing['pages'].extend(crawler.pages)
                existing['metadata']['total_pages'] = len(existing['pages'])
                with open("gds_org_consolidated.json", 'w') as f:
                    json.dump(existing, f, indent=2, ensure_ascii=False)
                print(f"Merged {len(crawler.pages)} recovered pages into existing data.")
            except FileNotFoundError:
                crawler.export_json("gds_org_consolidated.json")

        # Update failed pages file
        if crawler.failed_pages:
            crawler.export_failed_pages("gds_failed_pages.json")
        else:
            print("All pages recovered! You can delete gds_failed_pages.json")
        return

    # Normal crawl mode
    crawler.crawl()

    # Export results
    md_path = crawler.export_markdown("gds_org_consolidated.md")
    json_path = crawler.export_json("gds_org_consolidated.json")

    # Export failed pages if any
    if crawler.failed_pages:
        crawler.export_failed_pages("gds_failed_pages.json")

    print(f"\nFiles created:")
    print(f"  - {md_path} (for Claude/LLM reading)")
    print(f"  - {json_path} (structured backup)")
    if crawler.failed_pages:
        print(f"  - gds_failed_pages.json ({len(crawler.failed_pages)} pages to retry)")
        print(f"\nTo retry failed pages later, run:")
        print(f"  python crawl_gds.py --retry")


if __name__ == "__main__":
    main()
