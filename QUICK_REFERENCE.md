# ShopGraph AI - Quick Reference Card

## 🚀 Quick Commands

### First Time Setup
```bash
# 1. Create venv
python -m venv venv
source venv/bin/activate

# 2. Install Python deps
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env - add GEMINI_API_KEY

# 4. Seed database
python seed_database.py

# 5. Build frontend
cd frontend && npm install && npm run build && cd ..

# 6. Run
python main.py
```

### Daily Development

```bash
# Backend only (with auto-reload)
source venv/bin/activate
python main.py

# Frontend dev mode (hot reload)
# Terminal 1:
python main.py

# Terminal 2:
cd frontend && npm run dev
```

---

## 📁 File Structure

```
ShopGraphAI/
├── main.py                # Run this! 🚀
├── frontend_routes.py     # Serves React
├── seed_database.py       # Seed DB
├── .env                   # Your config
├── venv/                  # Python env
├── backend/app/           # Backend code
│   └── graph/             # LangGraph ⭐
└── frontend/              # React app
    └── dist/              # Built files
```

---

## 🌐 URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Main App |
| http://localhost:8000/docs | API Docs |
| http://localhost:8000/api/v1 | API Base |
| http://localhost:8000/health | Health Check |
| http://localhost:5173 | Frontend Dev Server |

---

## 🔧 Common Tasks

### Seed Database
```bash
python seed_database.py
```

### Rebuild Frontend
```bash
cd frontend && npm run build && cd ..
```

### Check MongoDB
```bash
mongosh
use shopgraph_ai
db.products.countDocuments()
```

### View Logs
```bash
# Backend logs appear in terminal
python main.py

# Watch for these:
# ✓ Successfully connected to MongoDB
# ✓ Graph compiled successfully
# ✓ Serving frontend from: ...
```

### Kill Port 8000
```bash
lsof -ti:8000 | xargs kill -9
```

---

## 🎮 Test Prompts

```
"Find gaming laptops under $1500"
"Compare the first two"
"Only Samsung products"
"Order the cheapest one"
```

---

## 🐛 Quick Fixes

### Can't import backend
```bash
# Run from root!
pwd  # Should show .../ShopGraphAI
python main.py
```

### Frontend not found
```bash
cd frontend && npm run build && cd ..
```

### MongoDB error
```bash
brew services start mongodb-community
```

### Port in use
```bash
# Change in .env
PORT=8001
```

---

## 📚 Documentation

| Doc | For |
|-----|-----|
| **SETUP.md** | Full setup guide |
| **CLAUDE.md** | Architecture |
| **MIGRATION_GUIDE.md** | Old → New structure |
| **README_NEW_STRUCTURE.md** | Overview |

---

## 🔑 Environment Variables

Essential `.env` settings:

```env
GEMINI_API_KEY=your_key_here          # Required!
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=shopgraph_ai
PORT=8000
ENVIRONMENT=development
```

---

## 🛠️ Development Modes

### Mode 1: Full Integration (Production-like)
```bash
# Build frontend once
cd frontend && npm run build && cd ..

# Run unified server
python main.py

# Access: http://localhost:8000
```

### Mode 2: Hot Reload (Development)
```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend
cd frontend && npm run dev

# Access: http://localhost:5173
```

---

## 🔍 Debugging

### Check Import Paths
```bash
# Should work from root:
python -c "from backend.app.core.config import settings; print(settings.gemini_api_key[:10])"
```

### Verify Frontend Build
```bash
ls frontend/dist/
# Should show: index.html, assets/, etc.
```

### Test API Directly
```bash
curl http://localhost:8000/health
```

### View API Logs
Backend logs show graph execution:
```
=== CLASSIFY INTENT NODE ===
→ Routing to SEARCH SUBGRAPH
Found 3 products
```

---

## 📦 Python Packages

Main dependencies:
- `fastapi` - Web framework
- `langgraph` - Agent orchestration
- `langchain` - LLM utilities
- `google-generativeai` - Gemini API
- `motor` - Async MongoDB
- `pydantic` - Validation

Install all: `pip install -r requirements.txt`

---

## 🎯 Key Concepts

### LangGraph
- **State** - Data flows through nodes
- **Nodes** - Pure functions
- **Routing** - Python logic (not LLM!)
- **Subgraphs** - Nested workflows
- **Tools** - Agent actions
- **Checkpointer** - State persistence

### Architecture
- **API Layer** - FastAPI endpoints
- **Service Layer** - Business logic
- **Repository Layer** - Database access
- **Graph Layer** - LangGraph agent

---

## 🚨 When Something Breaks

1. ✅ Check you're in root directory
2. ✅ Check venv is activated
3. ✅ Check MongoDB is running
4. ✅ Check .env has GEMINI_API_KEY
5. ✅ Check frontend is built
6. ✅ Read error message carefully
7. ✅ Check logs for details

---

## 💡 Pro Tips

- Use `python main.py` for most development
- Build frontend only when testing integration
- Keep MongoDB running in background
- Watch backend logs to understand flow
- Use API docs at `/docs` for testing
- Study graph logs to learn LangGraph

---

## 📞 Get Help

- Setup issues → SETUP.md
- Architecture → CLAUDE.md
- Migration → MIGRATION_GUIDE.md
- API questions → http://localhost:8000/docs

---

**Everything in one command:**
```bash
source venv/bin/activate && python main.py
```

Then open http://localhost:8000 🚀
