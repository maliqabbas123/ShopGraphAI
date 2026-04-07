# ShopGraph AI 🛍️🤖

> **A production-quality AI shopping assistant built with LangGraph, FastAPI, and React**

An AI shopping assistant demonstrating **stateful, tool-using agents** with **LangGraph**. Single server setup serving both backend API and React frontend.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-FF4B4B?style=for-the-badge)

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Seed database (MongoDB must be running)
python seed_database.py

# 5. Build frontend
cd frontend && npm install && npm run build && cd ..

# 6. Run the application
python main.py

# Open http://localhost:8000
```

**That's it!** Both API and frontend are served from port 8000.

---

## 🏗️ Unified Architecture

### Single Server Setup

```
http://localhost:8000/
├── /                    → React Frontend (SPA)
├── /api/v1/            → FastAPI Backend
├── /docs               → API Documentation
└── /health             → Health Check
```

### Project Structure

```
ShopGraphAI/
├── main.py                    # 🚀 Main entry point
├── frontend_routes.py         # Serves React build
├── seed_database.py           # Database seeder
├── requirements.txt           # Python deps
├── .env                       # Configuration
│
├── backend/app/              # Backend code
│   ├── api/                  # REST endpoints
│   ├── graph/                # ⭐ LangGraph magic
│   │   ├── state/            # State definitions
│   │   ├── nodes/            # Node functions
│   │   ├── subgraphs/        # Workflows
│   │   ├── tools/            # Agent tools
│   │   └── builders/         # Graph assembly
│   ├── services/             # Business logic
│   └── repositories/         # Data access
│
└── frontend/                 # React app
    ├── src/                  # Source code
    └── dist/                 # Build output
```

---

## 🎯 What You'll Learn

### LangGraph Concepts

✅ **Graph State** - TypedDict flowing through nodes
✅ **Nodes** - Pure functions transforming state
✅ **Routing** - Python-based conditional logic
✅ **Subgraphs** - Nested workflows
✅ **Tools** - Agent action functions
✅ **Checkpointer** - State persistence

### Architecture Patterns

✅ **Layered Design** - API → Services → Repositories
✅ **Clean Code** - Modular, testable, documented
✅ **Production Ready** - Error handling, logging, validation
✅ **Full Stack** - Backend + Frontend integration

---

## 🎮 Features

### User Features
- 🔍 Natural language product search
- ⚖️ Product comparison
- 🎯 Multi-turn refinement
- 🛒 Order placement
- 💬 Conversational interface

### Developer Features
- 📚 Educational code with comments
- 🧪 Testable architecture
- 📦 Modular design
- 🔧 Easy to extend
- 📊 Observable execution

---

## 📖 Documentation

| Guide | Purpose |
|-------|---------|
| **[SETUP.md](./SETUP.md)** | Complete setup instructions |
| **[CLAUDE.md](./CLAUDE.md)** | Architecture deep dive |
| **[GETTING_STARTED.md](./GETTING_STARTED.md)** | Quick start tutorial |
| **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** | File organization |

---

## 🛠️ Development

### Backend Development

```bash
# Activate venv
source venv/bin/activate

# Run with auto-reload
python main.py
```

Backend runs on http://localhost:8000 with auto-reload.

### Frontend Development

**Option 1: Dev Server** (Hot reload)
```bash
cd frontend
npm run dev  # Runs on :5173
```

**Option 2: Production Build** (Test integration)
```bash
cd frontend
npm run build
cd ..
python main.py  # Serves from :8000
```

---

## 🔍 API Documentation

When running, visit:

**http://localhost:8000/docs**

Interactive Swagger UI with all endpoints.

---

## 🎯 Example Prompts

### Search
```
"Find gaming laptops under $1500"
"Show me phones with good cameras"
```

### Compare
```
"Compare the first two"
"Compare the top 3 products"
```

### Order
```
"Order the cheapest one"
"Buy the first product"
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'backend'"

Run from root directory with venv activated:
```bash
pwd  # Should be /path/to/ShopGraphAI
source venv/bin/activate
```

### "Frontend not built"

Build the frontend:
```bash
cd frontend && npm run build && cd ..
```

### MongoDB Connection Error

Start MongoDB:
```bash
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

More troubleshooting → [SETUP.md](./SETUP.md)

---

## 🎓 Learning Path

### Beginner
1. ✅ Run the app
2. ✅ Read [CLAUDE.md](./CLAUDE.md)
3. ✅ Study `backend/app/graph/builders/graph_builder.py`
4. ✅ Explore a subgraph

### Intermediate
1. ✅ Add a new intent
2. ✅ Create a custom tool
3. ✅ Build a new subgraph
4. ✅ Add product filters

### Advanced
1. ✅ Implement MongoDB checkpointer
2. ✅ Add streaming responses
3. ✅ Build custom inspector
4. ✅ Optimize graph execution

---

## 📊 Tech Stack

**Backend**
- FastAPI - Modern Python web framework
- LangGraph - Agent orchestration
- Google Gemini - LLM provider
- Motor - Async MongoDB driver
- Pydantic - Data validation

**Frontend**
- React 18 - UI library
- TypeScript - Type safety
- Vite - Build tool

**Database**
- MongoDB - Document database

---

## 🚀 Deployment

### Production Build

```bash
# Build frontend
cd frontend && npm run build && cd ..

# Set production environment
# Edit .env: ENVIRONMENT=production

# Run with gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📝 License

MIT License - Free to use for learning and portfolio.

---

## 🙏 Acknowledgments

- **LangChain Team** - For LangGraph
- **FastAPI** - For excellent framework
- **Google** - For Gemini API

---

## 📧 Support

- **Setup Help**: See [SETUP.md](./SETUP.md)
- **Architecture**: See [CLAUDE.md](./CLAUDE.md)
- **API Docs**: http://localhost:8000/docs

---

## 🔗 Quick Links

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [MongoDB Docs](https://www.mongodb.com/docs/)

---

**Built with ❤️ for learning LangGraph and building production-quality AI agents**

**Start now:** `python main.py` → http://localhost:8000 🚀
