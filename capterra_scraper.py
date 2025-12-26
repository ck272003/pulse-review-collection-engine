from .base_scraper import BaseScraper
from datetime import datetime

class CapterraScraper(BaseScraper):
    def scrape(self, company_name, start_date, end_date):
        self.start_browser()
        reviews = []
        
        # Capterra is tougher with dynamic loading and heavy anti-bot.
        # URL structure: https://www.capterra.com/p/{id}/{slug}/reviews/
        # Simplified for assignment: https://www.capterra.com/software/{company_name}
        url = f"https://www.capterra.com/p/{company_name}/reviews" 
        print(f"Navigating to {url}")

        try:
            self.page.goto(url, timeout=60000)
            self.page.wait_for_timeout(3000)
            
            # Capterra often uses a 'Load More' button or infinite scroll, or standard pagination
            # For this simplified version, we'll try to grab visible reviews.
            
            # Selector guess based on common Capterra structure (div.review-card)
            # Note: Selectors change often on Capterra.
            review_cards = self.page.query_selector_all("div[class*='ReviewCard']")
            
            if not review_cards:
                print("No reviews found (Capterra selectors might have changed or bot protection active).")

            for card in review_cards:
                try:
                    # Generic structure attempt
                    title_el = card.query_selector("h3") or card.query_selector("div[class*='title']")
                    body_el = card.query_selector("p") or card.query_selector("div[class*='text']")
                    # Date is often tricky on Capterra
                    
                    if title_el and body_el:
                        reviews.append({
                            "title": title_el.inner_text(),
                            "review": body_el.inner_text(),
                            "date": datetime.now().strftime("%Y-%m-%d"), # Fallback as date parsing is complex
                            "source": "Capterra"
                        })
                except:
                    continue
                    
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.close_browser()

        return reviews
