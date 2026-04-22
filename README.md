# Web Scraping with Scrapy

An introduction to structured web scraping using the **Scrapy** framework. Scrapes book data from [books.toscrape.com](http://books.toscrape.com) — a sandbox site built for scraping practice.

## What it scrapes

For each book on the site:
- Title
- Price
- Star rating
- Availability

Results are exported as JSON or CSV.

## Running it

```bash
cd part-3/bookscraper
pip install scrapy

# Run the spider and export to JSON
scrapy crawl bookspider -o books.json

# Or export to CSV
scrapy crawl bookspider -o books.csv
```

## Project structure

```
part-3/
└── bookscraper/
    ├── bookscraper/
    │   ├── spiders/
    │   │   └── bookspider.py   — main spider definition
    │   ├── items.py            — data model
    │   ├── middlewares.py      — request/response hooks
    │   ├── pipelines.py        — post-processing pipeline
    │   └── settings.py         — Scrapy config
    └── scrapy.cfg
```

## Tech

- Python 3
- Scrapy — spider framework, CSS/XPath selectors, item pipelines
