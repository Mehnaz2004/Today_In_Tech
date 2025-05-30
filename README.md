# ⚡ Today In Tech

🔍 Stay updated with the latest tech news from trusted sources like TechCrunch, The Verge, and Hacker News — personalized just for you.

---

## 🔖 Overview

**Today In Tech** is a full-stack web app that allows users to log in, scrape trending tech articles, and view them on a futuristic dashboard. Built with Flask, Firebase Auth, MongoDB Atlas, and deployed using **Render**, this platform makes web scraping seamless and personalized.

---

## ✨ Features

* 🔐 **Secure Authentication**
  Google + Email/Password login via Firebase

* 🪡 **Personalized Dashboards**
  Articles are linked to each user's Firebase UID

* ⏳ **Live Scraping**
  Scrape the latest tech news instantly with the **Scrape Now** button

* 🔄 **Real-Time Updates**
  Scraped articles show instantly with animations + success messages

* 🌌 **Modern Dark-Themed UI**
  Neon gradients, Orbitron fonts, and responsive Bootstrap layout

---

## 📄 Live Demo

✨ **Try it here:** [Live App on Render](https://today-in-tech.onrender.com/)

---

## 💠 Tech Stack

| Layer        | Tech                                     |
| ------------ | ---------------------------------------- |
| **Frontend** | HTML, Bootstrap 5, Vanilla JS            |
| **Backend**  | Flask (Python)                           |
| **Scraper**  | BeautifulSoup + Requests                 |
| **Database** | MongoDB Atlas                            |
| **Auth**     | Firebase Authentication                  |
| **Hosting**  | Render (Flask), Firebase (static assets) |

---

## 📅 Usage Flow

1. Log in with Google or Email/Password
2. Get redirected to `/dashboard`
3. Click **Scrape Now** to fetch latest tech headlines
4. Articles saved in MongoDB under your UID
5. View them in a paginated, searchable table

---

## 🛠️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Mehnaz2004/Today_In_Tech.git
cd Today_In_Tech
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Firebase Config

Create a Firebase project:

* Enable Email/Password + Google Auth
* Add your Firebase config in `static/js/firebase_config.js`

```js
const firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  projectId: "...",
  ...
};
```

### 4. Set MongoDB URI

Update your MongoDB URI in `app.py`:

```python
client = MongoClient("your-mongodb-uri")
```

### 5. Run the App

```bash
python app.py
```

Visit `http://localhost:5000`

---

## 📈 Dashboard Highlights

* Sticky navbar with user name and logout
* Table with title, author, source, date, and URL
* Loading overlay on scraping
* Success toast with article count

---

## 🚡 To-Do / Planned Features

* [ ] Search + Filter
* [ ] Bookmark articles
* [ ] Auto-scheduled scraping (cron jobs)
* [ ] Article summaries using NLP

---

## 👧 Author

**Mehnaz Ali**
🔗 [LinkedIn](https://www.linkedin.com/in/mehnaz-ali-7b4764282/)
💻 [GitHub](https://github.com/Mehnaz2004)

---

## 📜 License

MIT License — free to use and build upon!
