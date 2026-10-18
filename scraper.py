import datetime
import json
import feedparser
import requests

# Paste your Google Apps Script Web App URL between the quotes below:
GOOGLE_SHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwRrQlRfR8MfQy1OOeLEZI-LFNvYrYv91ijpeT4on0Iy_aM1kQ8pVEWKor4zGU-rR69QQ/exec"

SOURCES = {
    "ATD_News": "https://www.td.org/rss/news",
    "ELearningIndustry": "https://elearningindustry.com/feed",
    "ChiefLearningOfficer": "https://www.chieflearningofficer.com/feed/",
    "TrainingIndustry": "https://trainingindustry.com/feed/",
}

LD_KEYWORDS = [
    "learning and development",
    "upskilling",
    "reskilling",
    "ai in learning",
    "microlearning",
    "lms",
    "lxp",
    "instructional design",
    "workforce development",
    "leadership training",
    "capability building",
]

def run_scraper():
    print("Initializing Zero-Cost Global L&D Scraper...")
    all_articles = []

    for name, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "")
                link = entry.get("link", "")
                published = entry.get("published", str(datetime.date.today()))
                summary = entry.get("summary", "")

                content = f"{title} {summary}".lower()
                if any(kw in content for kw in LD_KEYWORDS):
                    all_articles.append({
                        "Source": name,
                        "Title": title,
                        "URL": link,
                        "Date": published
                    })
        except Exception as e:
            print(f"Error reading {name}: {e}")

    # Save locally to JSON
    with open("ld_latest_updates.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print(f"Success! Scraped {len(all_articles)} relevant L&D updates worldwide.")

    # Send data to Google Sheets via Webhook with a 15-second timeout safeguard
    if GOOGLE_SHEET_WEBHOOK_URL and GOOGLE_SHEET_WEBHOOK_URL != "YOUR_WEB_APP_URL_HERE":
        try:
            print("Sending updates to Google Sheets...")
            response = requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=all_articles, timeout=15)
            print(f"Google Sheets response: {response.status_code}")
        except Exception as e:
            print(f"Failed to send data to Google Sheets: {e}")

if __name__ == "__main__":
    run_scraper()
