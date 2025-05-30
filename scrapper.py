import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

header={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

def save_to_mongodb(articles, user_id=None, collection_name="articles"):
    """
    Saves new articles to MongoDB. Skips duplicates based on title or URL.
    If user_id is provided, saves the user_id with each article.
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
            # Attach user_id if given
            if user_id:
                article["user_id"] = user_id

            existing = collection.find_one({
                "$and": [
                    {"user_id": user_id} if user_id else {},
                    {"$or": [
                        {"title": article["title"]},
                        {"url": article["url"]}
                    ]}
                ]
            })

            if not existing:
                collection.insert_one(article)
                inserted_count += 1
                

        print(f"✅ Inserted {inserted_count} new article(s) to MongoDB.")

    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")

def scrape_techcrunch():
    articles = []
    page=requests.get("https://techcrunch.com/")
    soup = BeautifulSoup(page.text, 'html.parser')

    for card in soup.select('div.loop-card__content'):
        title_tag = card.find('a', class_='loop-card__title-link')
        time_tag = card.find('time')
        author_tag = card.select_one('a.loop-card__author')
        author = author_tag.get_text(strip=True) if author_tag else "Tech Crunch"

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        url = title_tag.get('href')

        if time_tag and time_tag.has_attr('datetime'):
            raw_date = time_tag['datetime']
            try:
                dt_object = datetime.fromisoformat(raw_date)
                formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        articles.append({
            "title": title,
            "url": url,
            "published_at": formatted_date,
            "author": author,
            "source": "TechCrunch"
        })

    return articles

def scrape_theverge():
    articles = []
    page=requests.get("https://www.theverge.com/tech")
    soup = BeautifulSoup(page.text, 'html.parser')

    for card in soup.select('div._1pm20r51'):
        title_tag = card.find('a', class_='_1lkmsmo1')
        time_tag = card.find('time')
        author_tag = card.select_one('span._1lldluw2._1xwtict5')
        author = author_tag.get_text(strip=True) if author_tag else "The Verge"

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        url = title_tag.get('href')

        if time_tag and time_tag.has_attr('datetime'):
            raw_date = time_tag['datetime']
            try:
                dt_object = datetime.fromisoformat(raw_date)
                formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        articles.append({
            "title": title,
            "url": url,
            "published_at": formatted_date,
            "author": author,
            "source": "The Verge"
        })

    return articles

def scrape_venturebeat():
    articles = []
    page = requests.get("https://venturebeat.com/category/ai/", headers=header)
    soup = BeautifulSoup(page.text, 'html.parser')

    for card in soup.select('header.ArticleListing__body '):
        title_tag = card.find('h2', class_='ArticleListing__title')
        time_tag = card.find('time')
        author_tag = card.find('a', class_='ArticleListing__author')

        if not title_tag or not title_tag.a:
            continue

        title = title_tag.get_text(strip=True)
        url = title_tag.a.get('href')
        author = author_tag.get_text(strip=True) if author_tag else "Venture Beat"

        if time_tag and time_tag.has_attr('datetime'):
            raw_date = time_tag['datetime']
            try:
                dt_object = datetime.fromisoformat(raw_date)
                formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        articles.append({
            "title": title,
            "url": url,
            "published_at": formatted_date,
            "author": author,
            "source": "VentureBeat"
        })

    return articles

def scrape_all(user_id=None):
    articles = []
    articles += scrape_techcrunch()
    articles += scrape_theverge()
    articles += scrape_venturebeat()
    save_to_mongodb(articles, user_id=user_id)
    return articles
