import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyD41-VckzDCse3K3M659iAyk5kMcOUnSN8",
  authDomain: "todayintech-f238a.firebaseapp.com",
  projectId: "todayintech-f238a",
  storageBucket: "todayintech-f238a.appspot.com",
  messagingSenderId: "484902409160",
  appId: "1:484902409160:web:16d8b86d681aa11baf66fd",
  measurementId: "G-C01K6XGZDJ"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

let idToken = "";
let articles = [];
let currentPage = 1;
const pageSize = 8;
let sortState = {
  title: null,
  author: null,
  published_at: null,
  source: null
};

function showOverlay(message) {
  document.getElementById("loadingOverlay").classList.remove("d-none");
  document.getElementById("loadingMessage").innerText = message;
  document.getElementById("dismissBtn").classList.add("d-none");
}

function hideOverlay(message) {
  document.getElementById("loadingMessage").innerText = message;
  document.getElementById("dismissBtn").classList.remove("d-none");
}

function sortArticles(field) {
  const state = sortState[field];
  Object.keys(sortState).forEach(k => sortState[k] = null); // reset all
  if (state === null) sortState[field] = "asc";
  else if (state === "asc") sortState[field] = "desc";
  else sortState[field] = null;

  const direction = sortState[field];

  if (direction) {
    articles.sort((a, b) => {
      const valA = (a[field] || "").toLowerCase();
      const valB = (b[field] || "").toLowerCase();
      return direction === "asc" ? valA.localeCompare(valB) : valB.localeCompare(valA);
    });
  }

  currentPage = 1;
  renderPage();
  updateSortIcons();
}

function updateSortIcons() {
  ["title", "author", "published_at", "source"].forEach(field => {
    const icon = document.getElementById(`${field}-sort`);
    const state = sortState[field];
    icon.textContent = state === "asc" ? "↑" : state === "desc" ? "↓" : "⇅";
  });
}

function renderPage() {
  const container = document.getElementById("articlesBody");
  const start = (currentPage - 1) * pageSize;
  const end = start + pageSize;

  // Render table rows for current page
  const rows = articles.slice(start, end).map((a) => `
    <tr>
      <td>${a.title || "—"}</td>
      <td><a href="${a.url || '#'}" target="_blank">Visit</a></td>
      <td>${a.author || "—"}</td>
      <td>${a.published_at || "—"}</td>
      <td>${a.source || "—"}</td>
    </tr>
  `).join("");

  container.innerHTML = rows;

  // Render pagination
  const pageCount = Math.ceil(articles.length / pageSize);
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  for (let i = 1; i <= pageCount; i++) {
    const li = document.createElement("li");
    li.className = `page-item ${i === currentPage ? "active" : ""}`;
    li.innerHTML = `<button class="page-link">${i}</button>`;
    li.addEventListener("click", () => {
      currentPage = i;
      renderPage();
    });
    pagination.appendChild(li);
  }
}


onAuthStateChanged(auth, async (user) => {
  if (!user) return (window.location.href = "/login");

  idToken = await user.getIdToken();
  document.getElementById("userName").innerText = `Welcome, ${user.displayName || "User"}`;

  const res = await fetch("/get-articles", {
    method: "POST",
    headers: { "Authorization": `Bearer ${idToken}` },
  });

  articles = await res.json();

  if (!articles.length) {
    document.getElementById("articles-container").innerHTML = `
      <div class="alert alert-info text-center">
        No articles yet.<br><strong>Click "Scrape Now" to get the latest tech headlines!</strong>
      </div>`;
    return;
  }

  renderPage();

  const latestTime = articles[0]?.published_at || "—";
  document.getElementById("lastUpdated").innerText = `Last Updated: ${latestTime}`;
});

document.getElementById("scrapeBtn").addEventListener("click", async () => {
  showOverlay("Scraping in progress...");

  const res = await fetch("/scrape-articles", {
    method: "POST",
    headers: { "Authorization": `Bearer ${idToken}` },
  });

  const { added } = await res.json();
  hideOverlay(`Successfully added ${added} new article${added !== 1 ? "s" : ""}`);
});

document.getElementById("dismissBtn").addEventListener("click", () => {
  document.getElementById("loadingOverlay").classList.add("d-none");
  location.reload();
});

document.getElementById("logoutBtn").addEventListener("click", async () => {
  await signOut(auth);
  window.location.href = "/";
});

["title", "author", "published_at", "source"].forEach(field => {
  document.getElementById(`${field}-header`).addEventListener("click", () => sortArticles(field));
});
