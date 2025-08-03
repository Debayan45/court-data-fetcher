# court-data-fetcher
A web app to fetch Indian court case data and display it in a mini dashboard.

# 🏛️ Court Data Fetcher & Mini Dashboard

A Flask-based web application that scrapes real-time court case data from the Indian eCourts portal (District Court: Faridabad), stores logs in a local database, and displays the results on a mini dashboard.

---

## 📌 Features

- 🔎 Fetches live case details (party names, filing dates, order PDFs) from court websites
- 🧾 Parses HTML responses using BeautifulSoup
- 🗃 Logs search history and raw responses into SQLite
- 🖥 Minimal Flask-based frontend UI
- 🔁 Graceful error handling for missing/invalid cases

---

## 🏛️ Court Targeted

- **Court**: Faridabad District Court, Haryana  
- **Source Site**: [eCourts Services - District Courts](https://districts.ecourts.gov.in/)

---

## 🛠️ Tech Stack

| Layer     | Tool                        |
|-----------|-----------------------------|
| Backend   | Flask (Python)              |
| Scraping  | `requests`, `BeautifulSoup` |
| Database  | SQLite (via `sqlite3`)      |
| Frontend  | HTML + Bootstrap (inline)   |
| Deployment| GitHub (Render-ready)       |

---

## 📦 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/Debayan45/court-data-fetcher.git
cd court-data-fetcher
