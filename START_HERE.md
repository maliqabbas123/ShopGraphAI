# 🚀 START HERE - ShopGraph AI

Welcome! This file will get you started quickly.

---

## ⚡ 3-Step Quick Start

### Step 1: Setup (5 minutes)
```bash
# From the ShopGraphAI root directory:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure (2 minutes)
```bash
# Create config file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get one here: https://makersuite.google.com/app/apikey
nano .env  # or use your favorite editor
```

### Step 3: Run (1 minute)
```bash
# Seed database (MongoDB must be running)
python seed_database.py

# Build frontend (includes Tailwind CSS)
cd frontend && npm install && npm run build && cd ..

# Start the app!
python main.py
```

**Open http://localhost:8000** and start chatting! 🎉

---

## 📚 Documentation Map

| If You Want To... | Read This |
|-------------------|-----------|
| **Get started quickly** | This file + QUICK_REFERENCE.md |
| **Complete setup guide** | SETUP.md |
| **Understand architecture** | CLAUDE.md |
| **Migrate from old structure** | MIGRATION_GUIDE.md |
| **Quick command reference** | QUICK_REFERENCE.md |
| **See what was changed** | RESTRUCTURE_SUMMARY.md |

---

## 🎮 Try These Prompts

Once the app is running at http://localhost:8000:

```
"Find gaming laptops under $1500"

"Compare the first two"

"Only Samsung products"

"Order the cheapest one"
```

---

## 🏗️ Project Structure (Simplified)

```
ShopGraphAI/
├── main.py              # 🚀 Run this!
├── .env                 # Your config
├── venv/                # Python environment
│
├── backend/app/         # Backend code
│   └── graph/           # ⭐ LangGraph magic here
│
└── frontend/            # React app
    └── dist/            # Built frontend
```

---

## 🔑 Key Commands

```bash
# Run the app
python main.py

# Seed database
python seed_database.py

# Build frontend
cd frontend && npm run build && cd ..

# Frontend dev mode (hot reload)
cd frontend && npm run dev
```

---

## 🐛 Common Issues

### Can't find 'backend' module
```bash
# Make sure you're in the root directory
pwd  # Should show .../ShopGraphAI
```

### Frontend not found
```bash
# Build it first
cd frontend && npm run build && cd ..
```

### MongoDB error
```bash
# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

---

## 📖 What This Project Teaches

✅ **LangGraph** - Building stateful AI agents
✅ **Graph State** - Managing complex workflows
✅ **Subgraphs** - Composing multi-step processes
✅ **Tools** - Agent capabilities
✅ **Clean Architecture** - Production patterns

---

## 🎯 Next Steps

1. ✅ Get it running (follow steps above)
2. ✅ Try the example prompts
3. ✅ Read CLAUDE.md to understand how it works
4. ✅ Study backend/app/graph/ to see LangGraph in action
5. ✅ Experiment with adding features

---

## 🆘 Need Help?

- **Setup issues?** → SETUP.md
- **Architecture questions?** → CLAUDE.md
- **Quick commands?** → QUICK_REFERENCE.md
- **API testing?** → http://localhost:8000/docs

---

## 🎓 Learning Path

**Beginner**
1. Run the app
2. Try different prompts
3. Read CLAUDE.md architecture guide

**Intermediate**
1. Study backend/app/graph/builders/graph_builder.py
2. Understand how nodes work
3. Try modifying a node

**Advanced**
1. Add a new intent
2. Create a custom tool
3. Build a new subgraph

---

**Everything you need is here. Start with the 3-Step Quick Start above!** 🚀

Questions? Check the docs or inspect the code - it's well-commented!
