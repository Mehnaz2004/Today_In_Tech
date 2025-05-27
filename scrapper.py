import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

articles=[]
header={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

load_dotenv()

def save_to_mongodb(articles, collection_name="articles"):
    """
    Saves new articles to MongoDB. Skips duplicates based on title or URL.
    """
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = "tech_articles"

    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[collection_name]

        if not articles:
            print("No articles to save.")
            return

        inserted_count = 0

        for article in articles:
            existing = collection.find_one({
                "$or": [
                    {"title": article["title"]},
                    {"url": article["url"]}
                ]
            })

            if not existing:
                collection.insert_one(article)
                inserted_count += 1
            else:
                print(f"⚠️ Duplicate found. Skipping: {article['title']}")

        print(f"✅ Inserted {inserted_count} new article(s) to MongoDB.")

    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")



def scrape_techcrunch():
    page=requests.get("https://techcrunch.com/")
    soup = BeautifulSoup(page.text, 'html.parser')
    
    for card in soup.select('div.loop-card__content'):
        # Extract title and URL
        title_tag = card.find('a', class_='loop-card__title-link')
        time_tag = card.find('time')

        if not title_tag:
            continue  # skip if title is missing

        title = title_tag.get_text(strip=True)
        url = title_tag.get('href')

        # Format date
        if time_tag and time_tag.has_attr('datetime'):
            raw_date = time_tag['datetime']
            try:
                dt_object = datetime.fromisoformat(raw_date)
                formatted_date = dt_object.strftime("%B %d, %Y")
            except Exception:
                formatted_date = datetime.now().strftime("%B %d, %Y")
        else:
            formatted_date = datetime.now().strftime("%B %d, %Y")

        articles.append({
            "title": title,
            "url": url,
            "published_at": formatted_date,
            "source": "TechCrunch"
        })

    return articles

articles = scrape_techcrunch()
save_to_mongodb(articles)