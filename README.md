# ShopGraph AI 🛍️🤖

> **A production-quality AI shopping assistant built with LangGraph, FastAPI, and React**

ShopGraph AI is a comprehensive learning project that demonstrates how to build a **stateful, tool-using AI agent** using **LangGraph**. This project showcases industry-standard patterns for building conversational AI applications that can perform complex, multi-step workflows.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-FF4B4B?style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)

---

## 🎯 Project Goals

This project is designed for **learning LangGraph concepts deeply through code**. It demonstrates:

✅ **Graph-based agent orchestration** with nodes, edges, and routing
✅ **Stateful conversations** with checkpointer/memory management
✅ **Tool-calling patterns** with real backend integration
✅ **Subgraph composition** for complex workflows
✅ **Production-ready architecture** with clean separation of concerns
✅ **Full-stack integration** from UI to database

**This is NOT a hackathon project.** The codebase is clean, modular, well-commented, and follows industry standards.

---

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────┐
│  React UI   │  ← User Interface (TypeScript + React)
└──────┬──────┘
       │ REST API
┌──────▼───────────────────────────────────┐
│         FastAPI Backend                  │
│  ┌────────────────────────────────────┐  │
│  │  LangGraph Agent                   │  │
│  │  ┌─────────────────────────────┐   │  │
│  │  │  Main Graph                 │   │  │
│  │  │  • Intent Classification    │   │  │
│  │  │  • Routing                  │   │  │
│  │  │  • Response Formatting      │   │  │
│  │  └─────────────────────────────┘   │  │
│  │  ┌─────────────────────────────┐   │  │
│  │  │  Subgraphs                  │   │  │
│  │  │  • Search Subgraph          │   │  │
│  │  │  • Comparison Subgraph      │   │  │
│  │  │  • Order Subgraph           │   │  │
│  │  └─────────────────────────────┘   │  │
│  │  ┌─────────────────────────────┐   │  │
│  │  │  Tools                      │   │  │
│  │  │  • search_products          │   │  │
│  │  │  • compare_products         │   │  │
│  │  │  • check_stock              │   │  │
│  │  │  • place_order              │   │  │
│  │  └─────────────────────────────┘   │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │  Repositories                      │  │
│  │  • ProductRepository               │  │
│  │  • OrderRepository                 │  │
│  │  • ChatSessionRepository           │  │
│  └────────────────────────────────────┘  │
└──────┬───────────────────────────────────┘
       │
┌──────▼──────┐
│   MongoDB   │  ← Data Persistence
└─────────────┘
```

### LangGraph Flow

```
User Input
    ↓
[Classify Intent Node] ← Uses Gemini to determine intent
    ↓
[Router Node] ← Python routing (deterministic)
    ├─→ "search" ──→ [Search Subgraph]
    ├─→ "compare" ─→ [Comparison Subgraph]
    ├─→ "order" ───→ [Order Subgraph]
    └─→ "chat" ────→ [General Chat Node]
    ↓
[Format Response Node]
    ↓
Output to User
```

**Key Insight:** Routing is done with **Python code**, not LLM calls, for speed and determinism.

---

## 🚀 Features

### For Users

- 🔍 **Natural Language Search**: "Find gaming laptops under $1500"
- ⚖️ **Product Comparison**: "Compare the top 3 options"
- 🎯 **Smart Refinement**: "Only Samsung" / "Only 256GB models"
- 🛒 **Easy Ordering**: "Order the cheapest one"
- 💬 **Conversational**: Remembers context across turns

### For Developers

- 📚 **Educational**: Extensive inline comments explaining why code exists
- 🧪 **Testable**: Clean architecture makes unit testing easy
- 📦 **Modular**: Clear separation between layers
- 🔧 **Extensible**: Easy to add new intents, tools, or subgraphs
- 📊 **Observable**: Detailed logging of graph execution

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm/yarn
- **MongoDB** running locally or a MongoDB URI
- **Google Gemini API key** ([Get one here](https://makersuite.google.com/app/apikey))

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ShopGraphAI
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=shopgraph_ai

# Gemini API Configuration (REQUIRED)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### Seed the Database

```bash
# Make sure MongoDB is running first!
python scripts/seed_database.py
```

You should see:

```
✓ Inserted 20 products
✓ Categories: laptop, phone, headphones, tablet, smartwatch, accessories
✓ Database seeding completed successfully!
```

#### Start the Backend

```bash
cd backend
python -m app.main
# Or with uvicorn:
uvicorn app.main:app --reload
```

Backend will be available at **http://localhost:8000**

API docs at **http://localhost:8000/docs**

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment

```bash
cp .env.example .env
```

The default configuration should work:

```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Start the Frontend

```bash
npm run dev
```

Frontend will be available at **http://localhost:5173**

---

## 🎮 Usage & Example Prompts

Once both backend and frontend are running, try these prompts:

### Search Examples

```
"Find gaming laptops under $1500"
"Show me phones with good cameras"
"Find wireless headphones"
"Show me budget tablets"
"Find Apple products"
```

### Comparison Examples

```
"Compare the first two"
"Compare the top 3 products"
"Which one has the best battery?"
"Compare all Apple products"
```

### Refinement Examples

```
"Only Samsung"
"Only products under $500"
"Show me options with rating above 4.5"
"Only in stock items"
```

### Order Examples

```
"Order the cheapest one"
"Buy the first product"
"Order the highest rated one"
"I want to buy the second option"
```

### General Chat

```
"Hello!"
"What can you do?"
"Tell me about the first product"
```

---

## 📁 Project Structure

```
ShopGraphAI/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/      # FastAPI route handlers
│   │   ├── core/                  # Config, logging, settings
│   │   ├── db/                    # MongoDB connection
│   │   ├── models/                # Data models (Product, Order, etc.)
│   │   ├── schemas/               # Request/response schemas
│   │   ├── repositories/          # Data access layer
│   │   ├── services/              # Business logic
│   │   ├── graph/                 # ⭐ LangGraph Implementation
│   │   │   ├── state/             # Graph state definitions
│   │   │   ├── nodes/             # Node functions
│   │   │   ├── subgraphs/         # Complex workflows
│   │   │   ├── tools/             # Agent tools
│   │   │   └── builders/          # Graph construction
│   │   └── main.py                # FastAPI app entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/            # Reusable React components
│   │   ├── features/              # Feature-specific modules
│   │   ├── services/              # API integration
│   │   ├── types/                 # TypeScript types
│   │   └── App.tsx                # Main app component
│   └── package.json
├── scripts/
│   ├── seed_data.json             # Sample product data
│   └── seed_database.py           # Database seeding script
├── CLAUDE.md                      # 📘 Detailed architecture documentation
└── README.md                      # This file
```

---

## 🧠 LangGraph Concepts Explained

### 1. Graph State

The `AgentState` is a TypedDict that flows through all nodes:

```python
class AgentState(TypedDict):
    messages: List[BaseMessage]       # Conversation history
    user_input: str                   # Current message
    intent: Optional[str]             # Classified intent
    products: Optional[List[Dict]]    # Search results
    selected_product: Optional[Dict]  # Product for ordering
    # ... more fields
```

**Why it matters:** State enables multi-turn conversations and context preservation.

### 2. Nodes

Nodes are **pure functions** that take state and return updates:

```python
async def classify_intent_node(state: AgentState) -> Dict[str, Any]:
    """Classify user intent using Gemini LLM."""
    user_input = state.get("user_input")
    intent = await gemini_service.classify_intent(user_input)
    return {"intent": intent}  # Partial update
```

**Why it matters:** Nodes are testable, composable, and single-responsibility.

### 3. Routing

Routing uses **Python logic** for deterministic decisions:

```python
def route_by_intent(state: AgentState) -> str:
    """Route to appropriate subgraph based on intent."""
    intent = state.get("intent")

    if intent == "search":
        return "search_subgraph"
    elif intent == "compare":
        return "comparison_subgraph"
    # ... etc
```

**Why Python over LLM:** Faster, deterministic, cost-effective, easier to debug.

### 4. Subgraphs

Subgraphs encapsulate multi-step workflows:

```python
# Search Subgraph
extract_filters → execute_search → format_response
```

**Why subgraphs:** Modularity, reusability, easier testing, clearer code structure.

### 5. Checkpointer

The checkpointer **persists state** between invocations:

```python
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# State is saved after each node execution
# Resume with same thread_id maintains context
```

**What gets checkpointed:**
- Complete conversation history
- Current search results
- Selected products
- Cart state

**Why it matters:** Enables conversation continuity and multi-turn interactions.

### 6. Tools

Tools are **decorated functions** the agent can call:

```python
@tool
async def search_products_tool(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    # ...
) -> Dict[str, Any]:
    """Search for products based on filters."""
    # Implementation
```

**Why it matters:** Clean interface between agent reasoning and actual operations.

---

## 🎓 Learning Path

### For Beginners

1. ✅ Run the app and test different prompts
2. ✅ Read `CLAUDE.md` for architecture overview
3. ✅ Study `backend/app/graph/builders/graph_builder.py` to see graph structure
4. ✅ Explore one subgraph (start with `search_subgraph.py`)
5. ✅ Modify a node to see effects

### For Intermediate

1. ✅ Add a new intent (e.g., "recommendations")
2. ✅ Create a custom tool
3. ✅ Build a new subgraph for a feature
4. ✅ Add additional product filters
5. ✅ Implement error handling improvements

### For Advanced

1. ✅ Replace MemorySaver with MongoDB checkpointer
2. ✅ Add streaming responses
3. ✅ Implement graph execution optimization
4. ✅ Build custom LangGraph inspector UI
5. ✅ Add A/B testing for prompts

---

## 🔍 Key Files to Study

| File | Purpose | Key Concepts |
|------|---------|--------------|
| `backend/app/graph/state/agent_state.py` | State definition | State management, TypedDict |
| `backend/app/graph/builders/graph_builder.py` | Graph assembly | Graph construction, checkpointer |
| `backend/app/graph/nodes/classify_intent.py` | Intent classification | LLM usage, node design |
| `backend/app/graph/nodes/route_decision.py` | Routing logic | Deterministic routing |
| `backend/app/graph/subgraphs/search_subgraph.py` | Search workflow | Subgraph patterns |
| `backend/app/graph/tools/search_tools.py` | Tool implementation | Tool design, @tool decorator |
| `backend/app/services/chat_service.py` | Business orchestration | Service layer, graph invocation |

---

## 🧪 Testing

### Backend Tests (Coming Soon)

```bash
cd backend
pytest tests/
```

### Example Test

```python
def test_classify_intent_node():
    state = {"user_input": "Find laptops", "messages": []}
    result = await classify_intent_node(state)
    assert result["intent"] == "search"
```

---

## 🚧 Production Considerations

This is a **development/learning project**. For production, consider:

### ✅ Already Implemented

- Clean architecture with separation of concerns
- Type hints and validation
- Structured logging
- Environment configuration
- Error handling basics

### ⚠️ Needs Enhancement for Production

1. **Persistent Checkpointer**: Replace `MemorySaver` with MongoDB/Redis
2. **Authentication**: Add user authentication and session management
3. **Rate Limiting**: Prevent API abuse
4. **Monitoring**: Add metrics, tracing, error tracking (Sentry)
5. **Caching**: Redis for frequent queries
6. **Database Indexes**: Optimize MongoDB queries
7. **Load Balancing**: Handle multiple instances
8. **CI/CD**: Automated testing and deployment
9. **Security**: Input sanitization, HTTPS, CORS hardening
10. **Scaling**: Horizontal scaling, message queues

---

## 📚 Documentation

- **[CLAUDE.md](./CLAUDE.md)**: Comprehensive architecture documentation
- **[API Docs](http://localhost:8000/docs)**: Automatic Swagger UI (when backend running)
- **Inline Comments**: Extensive comments in all key files

---

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **LangGraph**: Agent orchestration framework
- **LangChain**: LLM integration utilities
- **Google Gemini**: LLM provider
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server

### Database
- **MongoDB**: Document database

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Check if MongoDB is running
# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod

# Verify MongoDB connection
mongosh
```

### Frontend can't connect to backend

1. Check backend is running on port 8000
2. Verify `VITE_API_BASE_URL` in frontend `.env`
3. Check CORS settings in backend `.env`

### "Invalid Gemini API key"

1. Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Update `GEMINI_API_KEY` in `backend/.env`
3. Restart backend

### No products in search results

```bash
# Re-run seed script
python scripts/seed_database.py

# Verify in MongoDB
mongosh
use shopgraph_ai
db.products.countDocuments()  # Should return 20
```

---

## 🤝 Contributing

This is a learning project. Feel free to:

- Fork and experiment
- Add new features
- Improve documentation
- Share your learnings

---

## 📝 License

MIT License - Feel free to use this project for learning and portfolio purposes.

---

## 🙏 Acknowledgments

- **LangChain Team**: For LangGraph framework
- **FastAPI**: For excellent Python web framework
- **Google**: For Gemini API
- **React Team**: For React library

---

## 📧 Questions?

Study the code, read `CLAUDE.md`, and experiment! The best way to learn is by doing.

**Happy Learning!** 🚀

---

## 🔗 Quick Links

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [MongoDB Docs](https://www.mongodb.com/docs/)
- [Gemini API](https://ai.google.dev/)

---

**Built with ❤️ for learning LangGraph and building production-quality AI agents**
