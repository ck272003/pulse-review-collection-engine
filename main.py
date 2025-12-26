import argparse
import json
import os
import sys
from datetime import datetime

# Add the src directory to python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper.g2_scraper import G2Scraper
from src.scraper.capterra_scraper import CapterraScraper
from src.scraper.trustpilot_scraper import TrustpilotScraper


def parse_args():
    parser = argparse.ArgumentParser(description="Pulse Review Scraper")
    parser.add_argument("--company", required=True, help="Company name (slug)")
    parser.add_argument("--start_date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end_date", required=True, help="YYYY-MM-DD")
    parser.add_argument(
        "--source",
        required=True,
        choices=["g2", "capterra", "trustpilot"],
        help="Review source",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format")
        return

    print(f"🚀 Starting scrape for {args.company} on {args.source}...")
    print(f"📅 Date range: {args.start_date} to {args.end_date}")

    if args.source == "g2":
        scraper = G2Scraper(headless=True)
    elif args.source == "capterra":
        scraper = CapterraScraper(headless=True)
    else:
        scraper = TrustpilotScraper(headless=True)

    reviews = scraper.scrape(args.company, start_date, end_date)

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = f"{output_dir}/{args.source}_{args.company}_reviews.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(reviews)} reviews")
    print(f"📁 Output saved to {output_file}")


if __name__ == "__main__":
    main()
