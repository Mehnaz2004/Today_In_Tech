from flask import Flask, render_template, request, jsonify
from scrapper import scrape_all
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

load_dotenv()
app = Flask(__name__)

# Initialize Firebase Admin SDK (Make sure you have your Firebase service account JSON file)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["tech_articles"]
collection = db["articles"]

@app.route('/')
def landing():
    return render_template('index.html')  # CTA will link to /login

@app.route('/login')
def login_page():
    return render_template('auth.html')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# --- Verify Token Helper ---
def get_user_id_from_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token.get('uid')
    except Exception as e:
        print(f"❌ Token verification failed: {e}")
        return None
    
# --- Route to get articles ---
@app.route("/get-articles", methods=["POST"])
def get_articles():
    from pymongo import MongoClient

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify([])

    id_token = auth_header.split(" ")[1]
    user_id = get_user_id_from_token(id_token)

    if not user_id:
        return jsonify([])

    try:
        MONGO_URI = os.getenv("MONGO_URI")
        client = MongoClient(MONGO_URI)
        db = client["tech_articles"]
        collection = db["articles"]

        articles = list(collection.find(
    {"user_id": user_id},
    {
        "_id": 0,
        "title": 1,
        "url": 1,
        "source": 1,
        "author": 1,
        "published_at": 1
    }
))

        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/scrape-articles", methods=["POST"])
def scrape_articles():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    id_token = auth_header.split(" ")[1]
    user_id = get_user_id_from_token(id_token)

    if not user_id:
        return jsonify({"error": "Invalid token"}), 403

    try:
        articles = scrape_all(user_id=user_id)
        return jsonify({"message": f"Scraped {len(articles)} articles."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
