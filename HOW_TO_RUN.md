# 🚀 How to Run Aquamitra

## Quick Start - Full Stack (Backend + Frontend)

```bash
./start-all.sh
```

This will start:
- **Backend API** on http://localhost:8000
- **Frontend UI** on http://localhost:5173

Then open http://localhost:5173 in your browser!

---

## Backend Only

```bash
./run.sh
```

This will start only the backend server on http://localhost:8000

---

## What You'll See

```
=========================================
🚀 AQUAMITRA - Groundwater Data Assistant
=========================================

📁 Checking data files...
✅ Data directory exists
   Files: 4 CSV files found

🔑 Checking environment...
✅ .env file exists

🐍 Checking Python environment...
✅ Virtual environment exists
   Python: Python 3.11.14

=========================================
🚀 Starting FastAPI Server
=========================================

📍 Server will run on: http://localhost:8000
📍 API Documentation: http://localhost:8000/docs
📍 Health Check: http://localhost:8000/api/health

Press Ctrl+C to stop the server
```

---

## Test the API

### 1. Health Check
```bash
curl http://localhost:8000/api/health
```

### 2. Ask a Question (English)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "How many records are in the database?"}],
    "language": "en"
  }'
```

### 3. Ask in Hindi
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "कितने रिकॉर्ड हैं?"}],
    "language": "hi"
  }'
```

### 4. Get Supported Languages
```bash
curl http://localhost:8000/api/languages
```

---

## Interactive API Documentation

Open in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## Project Structure

```
Aquamitra/
├── run.sh              # 👈 Run this to start the server
├── server.py           # FastAPI server
├── rag_pipeline.py     # RAG logic with LlamaIndex
├── translation_service.py  # Multilingual support
├── .env                # API keys (Google Gemini)
├── .venv/              # Python virtual environment
└── data/
    └── ingres/         # CSV files (groundwater data)
        ├── groundwater_2021.csv
        ├── groundwater_2022.csv
        ├── groundwater_2023.csv
        └── groundwater_2024.csv
```

---

## Troubleshooting

### Port already in use?
```bash
lsof -ti:8000 | xargs kill -9
./run.sh
```

### Need to reinstall dependencies?
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Start from scratch?
```bash
rm -rf .venv
/usr/local/bin/python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run.sh
```

