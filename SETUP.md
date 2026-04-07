# ShopGraph AI - Setup Guide

This guide explains how to set up and run ShopGraph AI with the unified structure where both backend and frontend are served from a single server.

---

## 📁 Project Structure

```
ShopGraphAI/
├── main.py                    # 🚀 Main entry point (run this!)
├── frontend_routes.py         # Frontend serving logic
├── seed_database.py           # Database seeder
├── requirements.txt           # Python dependencies
├── .env                       # Your configuration (create from .env.example)
├── .env.example              # Environment template
│
├── backend/                   # Backend application code
│   └── app/
│       ├── api/              # API endpoints
│       ├── core/             # Configuration
│       ├── db/               # Database
│       ├── graph/            # ⭐ LangGraph (the magic!)
│       ├── models/           # Data models
│       ├── repositories/     # Data access
│       ├── schemas/          # Request/response schemas
│       ├── services/         # Business logic
│       └── utils/            # Utilities
│
├── frontend/                  # React application
│   ├── src/                  # Source code
│   ├── dist/                 # 📦 Build output (after npm run build)
│   └── package.json
│
├── scripts/
│   └── seed_data.json        # Sample products
│
└── venv/                      # Python virtual environment (you create this)
```

---

## ⚡ Quick Start (5 Minutes)

### 1. Prerequisites

Make sure you have:
- **Python 3.11+** installed
- **Node.js 18+** and npm
- **MongoDB** running locally
- **Gemini API key** ([Get here](https://makersuite.google.com/app/apikey))

### 2. Clone & Navigate

```bash
cd /path/to/ShopGraphAI
```

### 3. Backend Setup

```bash
# Create virtual environment in root
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_key_here
```

### 4. Seed the Database

Make sure MongoDB is running first!

```bash
# Start MongoDB (if not running)
brew services start mongodb-community  # macOS
# OR
sudo systemctl start mongod            # Linux

# Seed the database
python seed_database.py
```

You should see:
```
✓ Inserted 20 products
✓ Database seeding completed successfully!
```

### 5. Frontend Build

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Return to root
cd ..
```

This creates `frontend/dist/` with the production build.

### 6. Run the Application

```bash
# Make sure you're in root directory with venv activated
python main.py
```

You should see:
```
ShopGraph AI Backend Starting...
✓ Successfully connected to MongoDB database: shopgraph_ai
✓ Configured checkpointer (MemorySaver)
✓ Graph compiled successfully
Serving frontend from: /path/to/ShopGraphAI/frontend/dist
Application startup complete
```

### 7. Access the Application

Open your browser to:

**http://localhost:8000**

- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000/api/v1
- **Health Check**: http://localhost:8000/health

---

## 🔧 Development Workflow

### Backend Development

When working on backend code:

```bash
# Activate venv
source venv/bin/activate

# Run with auto-reload
python main.py

# Backend will reload automatically when you change Python files
```

### Frontend Development

For frontend development, you have two options:

#### Option A: Development Mode (Recommended for frontend work)

```bash
cd frontend

# Start Vite dev server
npm run dev
```

This runs frontend on http://localhost:5173 with hot reload.

The frontend will proxy API requests to http://localhost:8000 (configured in `frontend/vite.config.ts`).

**Run both:**
- Terminal 1: `python main.py` (backend on :8000)
- Terminal 2: `cd frontend && npm run dev` (frontend on :5173)

#### Option B: Production Mode (Test full integration)

```bash
# Build frontend
cd frontend
npm run build
cd ..

# Run main.py
python main.py
```

Access at http://localhost:8000 - both frontend and backend served together.

---

## 🗂️ Environment Configuration

### `.env` File

Create `.env` in the root directory:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=shopgraph_ai

# Gemini API (REQUIRED)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1

# CORS (for development)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8000

# Server
HOST=0.0.0.0
PORT=8000
```

---

## 🎮 Testing the Application

Once running at http://localhost:8000, try these prompts:

### Search
```
"Find gaming laptops under $1500"
"Show me phones with good cameras"
"Find wireless headphones"
```

### Compare
```
"Compare the first two"
"Compare the top 3 products"
"Which one has better battery?"
```

### Refine
```
"Only Samsung products"
"Only items under $500"
"Show me products rated above 4.5"
```

### Order
```
"Order the cheapest one"
"Buy the first product"
"Order the highest rated option"
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'backend'"

**Solution**: Make sure you're running from the root directory and venv is activated.

```bash
# Check current directory
pwd  # Should be /path/to/ShopGraphAI

# Activate venv
source venv/bin/activate

# Verify Python sees backend module
python -c "import backend.app.core.config"
```

### "Frontend not built" Error

**Solution**: Build the frontend first.

```bash
cd frontend
npm install
npm run build
cd ..
python main.py
```

### MongoDB Connection Error

**Solution**: Make sure MongoDB is running.

```bash
# Check if MongoDB is running
mongosh

# Start MongoDB if needed
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

### Port Already in Use

**Solution**: Change port or kill the process.

```bash
# Change port in .env
PORT=8001

# Or kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Gemini API Key Error

**Solution**: Verify your API key is correct.

1. Get a fresh key from https://makersuite.google.com/app/apikey
2. Update `GEMINI_API_KEY` in `.env`
3. Make sure no extra spaces or quotes
4. Restart the server

---

## 📦 Deployment

### Building for Production

```bash
# 1. Build frontend
cd frontend
npm run build
cd ..

# 2. Set production environment
# Edit .env:
ENVIRONMENT=production

# 3. Run with production server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Coming Soon)

A Dockerfile will be provided for containerized deployment.

---

## 🔍 Project Commands Reference

### Backend

```bash
# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Seed database
python seed_database.py

# Run with uvicorn directly
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install
npm install

# Development
npm run dev          # Dev server on :5173

# Production
npm run build        # Build to dist/
npm run preview      # Preview build

# Lint
npm run lint
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `frontend_routes.py` | Serves React build |
| `seed_database.py` | Seeds MongoDB with products |
| `.env` | Your configuration |
| `backend/app/graph/builders/graph_builder.py` | LangGraph setup |
| `backend/app/main.py` | ❌ **Not used anymore** (replaced by root `main.py`) |

---

## 🎓 Next Steps

1. ✅ **Run the app** - Follow quick start above
2. ✅ **Read CLAUDE.md** - Understand the architecture
3. ✅ **Study the graph** - Check `backend/app/graph/`
4. ✅ **Make changes** - Try adding features
5. ✅ **Learn LangGraph** - This is a learning project!

---

## 🆘 Getting Help

- **Architecture**: Read [CLAUDE.md](./CLAUDE.md)
- **Usage**: Read [README.md](./README.md)
- **Structure**: Read [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)
- **API Docs**: Visit http://localhost:8000/docs when running

---

## 🔄 Migration from Old Structure

If you had the old structure with `backend/app/main.py`:

### What Changed:
- ❌ **Old**: `backend/app/main.py`
- ✅ **New**: `main.py` (in root)

- ❌ **Old**: `backend/requirements.txt`
- ✅ **New**: `requirements.txt` (in root)

- ❌ **Old**: `backend/.env`
- ✅ **New**: `.env` (in root)

- ❌ **Old**: `backend/venv/`
- ✅ **New**: `venv/` (in root)

- ❌ **Old**: Frontend runs separately on :5173
- ✅ **New**: Frontend served from backend (or dev mode on :5173)

### Migration Steps:

```bash
# 1. Move/copy your .env to root
cp backend/.env .env

# 2. Create new venv in root
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Build frontend
cd frontend
npm run build
cd ..

# 5. Run from root
python main.py
```

---

**You're ready to go! 🚀**

Run `python main.py` and visit http://localhost:8000
