import datetime
import json
import feedparser
import requests

GOOGLE_SHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwEeSi2rX4DWfPIRIrfIlYDflDXxpPV8_iwHN9tCJwEJhLLh1F_kBsOJJ0G7Ned30X-3w/exec"

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

    with open("ld_latest_updates.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print(f"Success! Scraped {len(all_articles)} relevant L&D updates worldwide.")

if __name__ == "__main__":
    run_scraper()
