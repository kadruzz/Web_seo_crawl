import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" 
from django.core.management.base import BaseCommand
from crawler.models import Domain, Page, Insight
from urllib.parse import urljoin, urlparse
from collections import deque, Counter
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import nltk
from nltk.corpus import stopwords




nltk.download('stopwords')


class Command(BaseCommand):
    help = "Crawl a domain and extract SEO insights"

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **kwargs):
        domain_name = kwargs['domain'].replace("https://", "").replace("http://", "").strip()
        base_url = f"https://{domain_name}"

        self.stdout.write(self.style.SUCCESS(f"Starting crawl for: {base_url}"))

     
        domain_obj, _ = Domain.objects.get_or_create(domain_name=domain_name)

        visited = set()
        queue = deque([base_url])

        stop_words = set(stopwords.words('english'))

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page_browser = browser.new_page()

            while queue:
                url = queue.popleft()

                url = url.split("#")[0].rstrip("/")

                if url in visited:
                    continue
                visited.add(url)

                try:
                    try:
                        response = requests.get(url, timeout=10)
                        status_code = response.status_code
                    except:
                        status_code = 0
                    try:
                        page_browser.goto(url, timeout=60000)
                        html = page_browser.content()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Playwright failed: {url}"))
                        continue

                    soup = BeautifulSoup(html, 'html.parser')

                    title = soup.title.string.strip() if soup.title and soup.title.string else ""

                    meta = soup.find("meta", attrs={"name": "description"})
                    meta_desc = meta.get("content", "").strip() if meta else ""

                    h1 = [h.get_text(strip=True) for h in soup.find_all('h1')]
                    h2 = [h.get_text(strip=True) for h in soup.find_all('h2')]
                    h3 = [h.get_text(strip=True) for h in soup.find_all('h3')]

        
                    p_count = len(soup.find_all('p'))
                    img_count = len(soup.find_all('img'))

        
                    links = soup.find_all('a', href=True)

                    internal_links = 0
                    external_links = 0

                    for link in links:
                        href = link.get('href')

                        if not href or href.startswith("javascript") or href.startswith("mailto"):
                            continue

                        full_url = urljoin(base_url, href)
                        parsed_url = urlparse(full_url)

                        clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}".rstrip("/")

                        if domain_name in parsed_url.netloc:
                            internal_links += 1

                            if clean_url not in visited:
                                queue.append(clean_url)
                        else:
                            external_links += 1

                    text = soup.get_text(separator=" ").lower()
                    words = text.split()

                    words = [
                        w for w in words
                        if w.isalpha() and w not in stop_words and len(w) > 2
                    ]

                    total_words = len(words)
                    freq = Counter(words)

                    top_keywords = freq.most_common(10)

                    keywords = []
                    for word, count in top_keywords:
                        density = (count / total_words) * 100 if total_words else 0
                        keywords.append({
                            "keyword": word,
                            "density": round(density, 2)
                        })


                    page_obj, created = Page.objects.get_or_create(
                        domain=domain_obj,
                        url=url,
                        defaults={"status_code": status_code}
                    )

                    Insight.objects.update_or_create(
                        page=page_obj,
                        defaults={
                            "title": title,
                            "meta_description": meta_desc,
                            "h1": h1,
                            "h2": h2,
                            "h3": h3,
                            "p_count": p_count,
                            "image_count": img_count,
                            "internal_links": internal_links,
                            "external_links": external_links,
                            "keywords": keywords
                        }
                    )

                    self.stdout.write(self.style.SUCCESS(f"✔ Crawled: {url}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"✖ Error: {url} - {str(e)}"))

            browser.close()

        self.stdout.write(self.style.SUCCESS("✅ Crawling completed"))