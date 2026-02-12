# 🪟 Windows Setup Guide for Aquamitra

Complete step-by-step guide to run Aquamitra on Windows laptop.

---

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.11** installed (NOT 3.12 or 3.13)
- **Node.js 18+** and **npm** installed
- **Git** installed

---

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository (if not already done)

```cmd
git clone https://github.com/Sujalvasale8/Aquamitra.git
cd Aquamitra
```

---

### Step 2: Check Python Version

```cmd
python --version
```

**Expected output**: `Python 3.11.x`

**If you have Python 3.12 or 3.13**, you need to install Python 3.11:
- Download from: https://www.python.org/downloads/release/python-3119/
- During installation, check "Add Python to PATH"

---

### Step 3: Create Virtual Environment

```cmd
python -m venv .venv
```

---

### Step 4: Activate Virtual Environment

```cmd
.venv\Scripts\activate
```

**You should see** `(.venv)` at the beginning of your command prompt.

---

### Step 5: Upgrade pip

```cmd
python -m pip install --upgrade pip
```

---

### Step 6: Install Python Dependencies

```cmd
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI
- LlamaIndex with Groq integration
- DuckDB
- Sentence Transformers
- And more...

**Note**: This may take 5-10 minutes depending on your internet speed.

---

### Step 7: Create `.env` File

Create a new file named `.env` in the project root directory:

```cmd
copy .env.example .env
```

Then edit `.env` file with Notepad:

```cmd
notepad .env
```

Add your API keys:

```
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
HF_TOKEN=your_huggingface_token_here
```

**Where to get API keys:**
- **Groq API Key**: https://console.groq.com/keys (Free tier: 100k tokens/day)
- **Google API Key**: https://aistudio.google.com/app/apikey (For translation service)
- **HuggingFace Token**: https://huggingface.co/settings/tokens (Free)

Save and close Notepad.

---

### Step 8: Install Frontend Dependencies

Open a **NEW** Command Prompt window and navigate to the project:

```cmd
cd path\to\Aquamitra
cd chatbot-ui
npm install
```

---

### Step 9: Start the Backend Server

In the **FIRST** Command Prompt (with virtual environment activated):

```cmd
python server.py
```

**Expected output:**
```
🔑 Groq API key loaded
🤖 Models initialized (Groq + Llama 3.3)
🔄 Loading CSV files...
✅ Loaded 21142 rows into assessments
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this window open!** The backend server is now running.

---

### Step 10: Start the Frontend Server

In the **SECOND** Command Prompt window:

```cmd
cd chatbot-ui
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Keep this window open too!**

---

### Step 11: Open the Application

Open your web browser and go to:

```
http://localhost:5173
```

You should see the Aquamitra chatbot interface! 🎉

---

## 🧪 Test the Chatbot

Try these questions to verify everything is working:

1. **"How many total records are in the database?"**
   - Expected: 21,142 records

2. **"What is the average rainfall in Madhya Pradesh?"**
   - Expected: ~1047.32 mm

3. **"Show me top 5 districts with highest groundwater usage"**
   - Expected: List of 5 districts with aggregated usage

4. **"Show me areas in Madhya Pradesh where groundwater is being sustainably managed"**
   - Expected: List of safe areas in Madhya Pradesh

---

## 🛑 How to Stop the Servers

### Stop Backend Server:
- Go to the first Command Prompt window
- Press `Ctrl + C`

### Stop Frontend Server:
- Go to the second Command Prompt window
- Press `Ctrl + C`

---

## 🔄 How to Restart

### Next time you want to run the project:

**Terminal 1 (Backend):**
```cmd
cd path\to\Aquamitra
.venv\Scripts\activate
python server.py
```

**Terminal 2 (Frontend):**
```cmd
cd path\to\Aquamitra\chatbot-ui
npm run dev
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Python not found"
**Solution**: Install Python 3.11 and add to PATH during installation.

### Issue 2: "pip not found"
**Solution**: 
```cmd
python -m ensurepip --upgrade
```

### Issue 3: "Node not found"
**Solution**: Install Node.js from https://nodejs.org/

### Issue 4: Port 8000 already in use
**Solution**: Kill the process using port 8000:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Issue 5: Port 5173 already in use
**Solution**: Kill the process using port 5173:
```cmd
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F
```

### Issue 6: "Module not found" errors
**Solution**: Make sure virtual environment is activated and reinstall:
```cmd
.venv\Scripts\activate
pip install -r requirements.txt
```

### Issue 7: Groq API Rate Limit
**Error**: "Rate limit reached for model llama-3.3-70b-versatile"
**Solution**: Wait 1-2 minutes or upgrade to Groq Dev Tier

---

## 📁 Project Structure

```
Aquamitra/
├── server.py              # FastAPI backend server
├── rag_pipeline.py        # RAG logic with Groq LLM
├── translation_service.py # Multilingual support
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create this)
├── .env.example          # Example environment file
├── data/
│   └── ingres/           # CSV data files
│       ├── groundwater_2021.csv
│       ├── groundwater_2022.csv
│       ├── groundwater_2023.csv
│       └── groundwater_2024.csv
└── chatbot-ui/           # React frontend
    ├── package.json
    ├── src/
    │   ├── App.jsx       # Main React component
    │   └── ...
    └── ...
```

---

## 🎯 Supported Languages

The chatbot supports 7 Indian languages:
- English (en)
- Hindi (hi)
- Marathi (mr)
- Gujarati (gu)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)

---

## ✅ Success Checklist

- [ ] Python 3.11 installed
- [ ] Node.js installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed
- [ ] `.env` file created with API keys
- [ ] Frontend dependencies installed
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] Browser opened to http://localhost:5173
- [ ] Test queries working correctly

---

## 📞 Need Help?

If you encounter any issues:
1. Check the error messages in both Command Prompt windows
2. Verify all API keys are correct in `.env` file
3. Make sure Python 3.11 is being used (not 3.12 or 3.13)
4. Ensure both servers are running simultaneously

---

**Happy Testing! 🚀**

