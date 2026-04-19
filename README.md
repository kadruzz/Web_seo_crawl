# Website SEO Crawler & API

This project is a Django-based SEO crawler that scans a website and collects useful SEO data from each page. It uses Playwright to handle dynamic content and BeautifulSoup to extract information like titles, meta descriptions, headings, images, links, and keyword density.

The extracted data is stored in a database and exposed through simple REST APIs built with Django REST Framework. You can view all crawled domains, their pages, and detailed SEO insights for each page.

## Setup

1. Install dependencies:
   pip install django djangorestframework playwright beautifulsoup4 requests nltk

2. Install Playwright browsers:
   python -m playwright install

3. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

4. Start server:
   python manage.py runserver

## Usage

Run crawler:
python manage.py crawl example.com

Access APIs:

* /api/domains/
* /api/domains/{id}/pages/
* /api/pages/{id}/insights/

## Notes

* Works with dynamic websites
* Uses keyword analysis for SEO insights
* Avoid crawling very large sites without limits
