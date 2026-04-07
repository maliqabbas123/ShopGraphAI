# Getting Started with ShopGraph AI 🚀

Welcome! This guide will get you up and running in **5 minutes**.

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Get Your Gemini API Key (2 min)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the key - you'll need it in Step 3

### Step 2: Start MongoDB (1 min)

```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Windows
# Start MongoDB service from Services
# Or run: mongod
```

Verify it's running:
```bash
mongosh
# Should connect successfully
```

### Step 3: Setup Backend (1 min)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=your_key_here
```

Seed the database:
```bash
python scripts/seed_database.py
```

Start the backend:
```bash
python -m app.main
```

✅ Backend running at **http://localhost:8000**

### Step 4: Setup Frontend (1 min)

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start dev server
npm run dev
```

✅ Frontend running at **http://localhost:5173**

---

## 🎮 Try It Out!

Open http://localhost:5173 and try these prompts:

### 1. Search
```
"Find gaming laptops under $1500"
```

### 2. Compare
```
"Compare the first two"
```

### 3. Refine
```
"Only Apple products"
```

### 4. Order
```
"Order the cheapest one"
```

---

## 📚 Next Steps

### Learn the Architecture

1. **Read** [CLAUDE.md](./CLAUDE.md) - Comprehensive architecture guide
2. **Explore** [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - File organization
3. **Study** `backend/app/graph/builders/graph_builder.py` - See how the graph is built

### Understand LangGraph

Key files to study:

```
📁 backend/app/graph/
   ├── 📄 state/agent_state.py        ← Start here: State definition
   ├── 📁 nodes/                      ← Node functions
   ├── 📁 subgraphs/                  ← Complex workflows
   ├── 📁 tools/                      ← Agent capabilities
   └── 📁 builders/graph_builder.py   ← Graph assembly
```

### Experiment

Try making these changes:

1. **Add a new product attribute**
   - Edit `scripts/seed_data.json`
   - Re-run seed script
   - Search for products with that attribute

2. **Add a new intent**
   - Add intent in `classify_intent_node`
   - Create routing case in `route_decision.py`
   - Build a handler node

3. **Create a new tool**
   - Add tool in `backend/app/graph/tools/`
   - Use `@tool` decorator
   - Call from a node

---

## 🔍 API Documentation

While backend is running, visit:

**http://localhost:8000/docs**

Interactive Swagger UI with all endpoints documented.

---

## 💡 Tips

### Backend Logs

The backend logs show exactly what's happening:

```
=== CLASSIFY INTENT NODE ===
User input: 'Find gaming laptops'
Classified intent: search
→ Routing to SEARCH SUBGRAPH
=== EXTRACT FILTERS NODE ===
Extracted filters: {'category': 'laptop', 'tags': ['gaming']}
Found 3 products
```

Watch these logs to understand the graph flow!

### Frontend Developer Tools

Open browser DevTools → Console to see:
- API requests/responses
- State updates
- Errors

### Database Inspection

```bash
mongosh
use shopgraph_ai
db.products.find().pretty()
db.chat_sessions.find().pretty()
```

---

## 🐛 Troubleshooting

### "Connection refused" errors

- ✅ Check MongoDB is running: `mongosh`
- ✅ Check backend is running on port 8000
- ✅ Check no port conflicts

### "Invalid API key"

- ✅ Verify `GEMINI_API_KEY` in `backend/.env`
- ✅ Make sure no extra spaces
- ✅ Restart backend after changing `.env`

### No products found

```bash
# Re-run seed script
cd backend
python scripts/seed_database.py
```

### Frontend can't reach backend

- ✅ Check `VITE_API_BASE_URL` in `frontend/.env`
- ✅ Verify CORS settings in `backend/.env`
- ✅ Clear browser cache

---

## 🎯 What to Focus On

### For Learning LangGraph:

1. **State flow**: How `AgentState` moves through nodes
2. **Routing**: Why we use Python instead of LLM
3. **Subgraphs**: How they encapsulate workflows
4. **Checkpointing**: What gets persisted and why
5. **Tools**: How the agent performs actions

### For Understanding Architecture:

1. **Layered design**: API → Services → Repositories → Database
2. **Separation of concerns**: Each module has one job
3. **Type safety**: Pydantic models everywhere
4. **Error handling**: Try/catch patterns
5. **Testing patterns**: How to test nodes in isolation

---

## 📖 Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React Docs](https://react.dev/)
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)

---

## 🎓 Learning Challenges

Try implementing these features:

### Easy
- [ ] Add more products to seed data
- [ ] Change UI colors/styling
- [ ] Add new product categories

### Medium
- [ ] Add a "recommendation" intent
- [ ] Create a tool to get product details by ID
- [ ] Add pagination to product results

### Hard
- [ ] Replace MemorySaver with MongoDB checkpointer
- [ ] Add streaming responses
- [ ] Implement user authentication
- [ ] Add product images

---

## 🚀 You're Ready!

The app is running. Now it's time to:

1. ✅ Test all the features
2. ✅ Read the architecture docs
3. ✅ Study the code
4. ✅ Make modifications
5. ✅ Build something new!

**Happy Learning!** 🎉

---

Questions? Check:
- [README.md](./README.md) - Complete guide
- [CLAUDE.md](./CLAUDE.md) - Architecture deep dive
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - File organization

**Built with ❤️ for learning LangGraph**
