# Pulse Review Scraper

A Python-based web scraping tool that collects SaaS product reviews from
G2, Capterra, and Trustpilot for a given company and time period.

## Features
- Scrapes reviews from multiple platforms
- Supports date-range filtering
- Outputs structured JSON
- Handles pagination and errors gracefully
- Easily extensible to new sources

## Tech Stack
- Python 3.11+
- Playwright
- BeautifulSoup (optional)
- JSON

## Installation
```bash
cd pulse-review-scraper
pip install -r requirements.txt
playwright install
```

## Usage
```bash
python src/main.py \
  --company slack \
  --start_date 2024-01-01 \
  --end_date 2024-06-30 \
  --source g2
```

## Output Format
```json
{
  "title": "Great product",
  "review": "Very useful for teams...",
  "date": "2024-03-12",
  "rating": 5,
  "reviewer": "Product Manager",
  "source": "G2"
}
```

## Bonus Source
Trustpilot is integrated as a third SaaS review platform.

## Assumptions
- Publicly available reviews only
- Rate limits handled via delays

## Limitations
- Dynamic selector changes may require updates
- CAPTCHA-protected pages are skipped
