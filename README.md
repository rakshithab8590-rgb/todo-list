# TaskFlow — Railway Deployment Guide

## 📁 Project Structure
```
railway_todo/
├── app.py               ← Main Flask app (all routes + DB logic)
├── templates/
│   └── index.html       ← Frontend UI
├── requirements.txt     ← Python packages (flask, psycopg2, gunicorn)
├── Procfile             ← Tells Railway: run gunicorn
├── railway.toml         ← Railway config
└── .gitignore           ← Files to ignore in git
```

---

## 🚀 Step-by-Step Deploy on Railway

### STEP 1 — Install Git (if not installed)
Download from: https://git-scm.com/downloads

### STEP 2 — Create GitHub Account
Go to: https://github.com and sign up

### STEP 3 — Create a new GitHub Repository
1. Click "New" on GitHub
2. Name it: `taskflow-app`
3. Keep it Public
4. Click "Create repository"

### STEP 4 — Push your code to GitHub
Open terminal/cmd inside your project folder and run:

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/taskflow-app.git
git push -u origin main
```

### STEP 5 — Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Click "Deploy from GitHub Repo"
5. Select your `taskflow-app` repo
6. Click "Deploy Now" → Railway starts building ✅

### STEP 6 — Add PostgreSQL Database
1. In your Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway creates the database automatically

### STEP 7 — Connect Database to App
1. Click on your PostgreSQL service
2. Go to "Connect" tab
3. Copy the "DATABASE_URL" value
4. Click on your Flask app service
5. Go to "Variables" tab
6. Click "+ New Variable"
7. Name: `DATABASE_URL`
8. Value: paste the URL you copied
9. Click "Add" → Railway auto-redeploys ✅

### STEP 8 — Get your Live URL!
1. Click on your Flask app service
2. Go to "Settings" tab
3. Under "Domains" click "Generate Domain"
4. You get a URL like: `https://taskflow-app-production.up.railway.app` 🎉

---

## 🔧 How the Code Works

```
User clicks button
      ↓
Flask (app.py) receives request
      ↓
psycopg2 connects to PostgreSQL
      ↓
SQL query runs (INSERT / SELECT / DELETE)
      ↓
Data saved in Railway PostgreSQL
      ↓
Flask redirects back to homepage
```

## 📦 What each file does

| File | What it does |
|------|-------------|
| `app.py` | All Python logic — routes, DB connection, SQL queries |
| `templates/index.html` | The web page users see |
| `requirements.txt` | List of Python packages Railway installs |
| `Procfile` | Tells Railway how to start the app |
| `railway.toml` | Railway build configuration |
| `.gitignore` | Files NOT to upload to GitHub |

## 🆘 Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| App crashes on start | Check DATABASE_URL is set in Variables |
| "Module not found" error | Check requirements.txt has all packages |
| Changes not showing | Push to GitHub again: `git add . && git commit -m "update" && git push` |
| Database error | Make sure PostgreSQL service is running in Railway |
