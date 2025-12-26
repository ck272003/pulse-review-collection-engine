from .base_scraper import BaseScraper
from datetime import datetime

class TrustpilotScraper(BaseScraper):
    def scrape(self, company_name, start_date, end_date):
        self.start_browser()
        reviews = []

        # Trustpilot URL structure usually involves the domain. 
        # For this assignment we assume company_name is the domain or slug.
        # Often it's 'company.com'
        url = f"https://www.trustpilot.com/review/{company_name}"
        print(f"Navigating to {url}")

        try:
            self.page.goto(url, timeout=60000)
            self.page.wait_for_timeout(2000)

            while True:
                try:
                    self.page.wait_for_selector("article", timeout=10000)
                except:
                    print("No reviews found or timeout.")
                    break

                cards = self.page.query_selector_all("article")
                print(f"Found {len(cards)} reviews on this page.")

                for card in cards:
                    try:
                        title_el = card.query_selector("h2")
                        body_el = card.query_selector("p[data-service-review-text-typography='true']")
                        time_el = card.query_selector("time")

                        if not (title_el and time_el):
                             # Sometimes title is missing or structure varies
                             continue
                        
                        title = title_el.inner_text()
                        body = body_el.inner_text() if body_el else ""
                        date_text = time_el.get_attribute("datetime")
                        
                        if not date_text:
                            continue

                        review_date = datetime.fromisoformat(date_text.replace("Z", ""))

                        if start_date <= review_date <= end_date:
                            reviews.append({
                                "title": title,
                                "review": body,
                                "date": review_date.strftime("%Y-%m-%d"),
                                "source": "Trustpilot"
                            })
                    except Exception as e:
                        continue

                # Pagination
                next_button = self.page.query_selector("a[name='pagination-button-next']")
                if not next_button or next_button.is_disabled():
                    break
                
                next_button.click()
                self.page.wait_for_timeout(2000)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.close_browser()
            
        return reviews
