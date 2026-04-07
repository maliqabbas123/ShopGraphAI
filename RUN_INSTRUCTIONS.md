# 🚀 Quick Run Instructions

## ✅ Setup Complete!

Database seeded with 20 products. Now you can run the application.

---

## Run the Application

### Option 1: Serve Both Frontend & Backend (Production Mode)

```bash
# Make sure you're in the root directory
cd /home/malik_abbas/Documents/WORKSPACE/ShopGraphAI

# Activate virtual environment
source venv/bin/activate

# Build frontend first (one time)
cd frontend
npm install
npm run build
cd ..

# Run the application
python main.py

# Open in browser: http://localhost:8000
```

### Option 2: Development Mode (Hot Reload for Frontend)

```bash
# Terminal 1: Run backend
cd /home/malik_abbas/Documents/WORKSPACE/ShopGraphAI
source venv/bin/activate
python main.py

# Terminal 2: Run frontend dev server
cd /home/malik_abbas/Documents/WORKSPACE/ShopGraphAI/frontend
npm run dev

# Backend: http://localhost:8000
# Frontend: http://localhost:5173 (with hot reload)
```

---

## First Time Setup (Frontend)

If you haven't installed frontend dependencies yet:

```bash
cd /home/malik_abbas/Documents/WORKSPACE/ShopGraphAI/frontend

# Install dependencies (includes Tailwind CSS)
npm install

# Build for production
npm run build

# Go back to root
cd ..
```

---

## Test the Application

Once running, try these prompts:

```
"Find gaming laptops under $1500"
"Compare the first two"
"Only Samsung products"
"Order the cheapest one"
```

---

## Quick Commands

```bash
# Run backend only
python main.py

# Build frontend
cd frontend && npm run build && cd ..

# Frontend dev mode
cd frontend && npm run dev

# Re-seed database
python seed_database.py
```

---

## URLs

| URL | What |
|-----|------|
| http://localhost:8000 | Main app (production build) |
| http://localhost:8000/docs | API documentation |
| http://localhost:8000/api/v1 | API endpoints |
| http://localhost:5173 | Frontend dev server (if running npm run dev) |

---

## What's Running?

When you run `python main.py`:

✅ FastAPI backend on port 8000
✅ React frontend served from /frontend/dist (if built)
✅ API endpoints at /api/v1/*
✅ Automatic API docs at /docs

---

## Next Steps

1. **Build frontend** (if not already done): `cd frontend && npm run build && cd ..`
2. **Run**: `python main.py`
3. **Open**: http://localhost:8000
4. **Chat** with the AI shopping assistant!

---

**Ready to go!** 🚀
