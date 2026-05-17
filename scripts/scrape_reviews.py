import os
import pandas as pd
from google_play_scraper import Sort, reviews_all

BANKS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

def scrape_bank_reviews():
    all_reviews = []

    for bank_name, app_id in BANKS.items():
        print(f"Scraping reviews for {bank_name} ({app_id})...")
        try:
            scraped = reviews_all(
                app_id,
                lang='en',
                country='et',
                sort=Sort.NEWEST
            )

            for review in scraped[:500]:
                all_reviews.append({
                    "review": review.get("content"),
                    "rating": review.get("score"),
                    "date": review.get("at"),
                    "bank": bank_name,
                    "source": "Google Play"
                })

        except Exception as e:
            print(f"Error scraping {bank_name}: {e}")

    df = pd.DataFrame(all_reviews)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/raw_reviews.csv", index=False)
    print(f"Scraping completed. Total scraped: {len(df)} rows.")
    
if __name__ == "__main__":
    scrape_bank_reviews()