from .base_scraper import BaseScraper
from datetime import datetime
import time

class G2Scraper(BaseScraper):
    def scrape(self, company_name, start_date, end_date):
        self.start_browser()
        reviews = []

        # Assuming standard G2 URL structure. Note: G2 has strong bot detection.
        url = f"https://www.g2.com/products/{company_name}/reviews"
        print(f"Navigating to {url}")
        
        try:
            self.page.goto(url, timeout=60000)
            # Basic bot check evasion - wait a bit
            self.page.wait_for_timeout(3000)
            
            # Check for bot detection or captcha
            if "captcha" in self.page.content().lower():
                print("Warning: CAPTCHA detected. Manual intervention might be required.")

            while True:
                # Wait for reviews to load
                try:
                    self.page.wait_for_selector("div.paper", timeout=10000)
                except:
                    print("No reviews found or timeout waiting for selector.")
                    break

                review_cards = self.page.query_selector_all("div.paper")
                print(f"Found {len(review_cards)} reviews on this page.")

                for card in review_cards:
                    try:
                        title_el = card.query_selector("h3")
                        body_el = card.query_selector("p")
                        time_el = card.query_selector("time")
                        
                        if not (title_el and body_el and time_el):
                            continue

                        title = title_el.inner_text()
                        body = body_el.inner_text()
                        date_text = time_el.get_attribute("datetime")
                        
                        if not date_text:
                            continue

                        review_date = datetime.fromisoformat(date_text.replace("Z", ""))

                        # Simple date filtering
                        if start_date <= review_date <= end_date:
                            reviews.append({
                                "title": title,
                                "review": body,
                                "date": review_date.strftime("%Y-%m-%d"),
                                "source": "G2"
                            })
                    except Exception as e:
                        # print(f"Error parsing card: {e}")
                        continue

                # Pagination logic
                next_button = self.page.query_selector("a.next_page")
                if not next_button or "disabled" in next_button.get_attribute("class", ""):
                    break

                next_button.click()
                self.page.wait_for_timeout(2000) # Random delay ideally
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
        finally:
            self.close_browser()
            
        return reviews
