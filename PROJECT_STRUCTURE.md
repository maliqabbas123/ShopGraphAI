# ShopGraph AI - Complete Project Structure

```
ShopGraphAI/
├── README.md                           # Main documentation
├── CLAUDE.md                           # Detailed architecture guide
├── .gitignore                          # Git ignore rules
├── PROJECT_STRUCTURE.md                # This file
│
├── backend/                            # Backend application
│   ├── .env.example                    # Environment template
│   ├── requirements.txt                # Python dependencies
│   │
│   └── app/                            # Main application package
│       ├── __init__.py
│       ├── main.py                     # FastAPI entry point
│       │
│       ├── api/                        # API layer
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       └── endpoints/
│       │           ├── __init__.py
│       │           └── chat.py         # Chat endpoints
│       │
│       ├── core/                       # Core configuration
│       │   ├── __init__.py
│       │   ├── config.py               # Settings management
│       │   └── logging.py              # Logging setup
│       │
│       ├── db/                         # Database connection
│       │   ├── __init__.py
│       │   └── mongodb.py              # MongoDB client
│       │
│       ├── models/                     # Data models
│       │   ├── __init__.py
│       │   ├── product.py              # Product model
│       │   ├── cart.py                 # Cart model
│       │   ├── order.py                # Order model
│       │   └── chat_session.py         # Chat session model
│       │
│       ├── schemas/                    # Request/response schemas
│       │   ├── __init__.py
│       │   └── chat.py                 # Chat API schemas
│       │
│       ├── repositories/               # Data access layer
│       │   ├── __init__.py
│       │   ├── product_repository.py   # Product queries
│       │   ├── cart_repository.py      # Cart operations
│       │   ├── order_repository.py     # Order operations
│       │   └── chat_session_repository.py  # Session storage
│       │
│       ├── services/                   # Business logic
│       │   ├── __init__.py
│       │   ├── gemini_service.py       # Gemini API wrapper
│       │   └── chat_service.py         # Chat orchestration
│       │
│       ├── graph/                      # ⭐ LangGraph implementation
│       │   ├── __init__.py
│       │   │
│       │   ├── state/                  # Graph state definitions
│       │   │   ├── __init__.py
│       │   │   └── agent_state.py      # Main state TypedDict
│       │   │
│       │   ├── nodes/                  # Node functions
│       │   │   ├── __init__.py
│       │   │   ├── classify_intent.py  # Intent classification
│       │   │   ├── route_decision.py   # Routing logic
│       │   │   ├── general_chat.py     # General responses
│       │   │   └── format_response.py  # Response formatting
│       │   │
│       │   ├── subgraphs/              # Complex workflows
│       │   │   ├── __init__.py
│       │   │   ├── search_subgraph.py      # Product search flow
│       │   │   ├── comparison_subgraph.py  # Comparison flow
│       │   │   └── order_subgraph.py       # Order placement flow
│       │   │
│       │   ├── tools/                  # Agent tools
│       │   │   ├── __init__.py
│       │   │   ├── search_tools.py         # Search & filter
│       │   │   ├── comparison_tools.py     # Product comparison
│       │   │   └── order_tools.py          # Cart & orders
│       │   │
│       │   └── builders/               # Graph construction
│       │       ├── __init__.py
│       │       └── graph_builder.py    # Main graph builder
│       │
│       └── utils/                      # Utility functions
│
├── frontend/                           # Frontend application
│   ├── .env.example                    # Environment template
│   ├── package.json                    # Node dependencies
│   ├── tsconfig.json                   # TypeScript config
│   ├── tsconfig.node.json             # Node TypeScript config
│   ├── vite.config.ts                  # Vite configuration
│   ├── index.html                      # HTML entry point
│   │
│   └── src/                            # Source code
│       ├── main.tsx                    # React entry point
│       ├── App.tsx                     # Main app component
│       ├── vite-env.d.ts              # Vite types
│       │
│       ├── components/                 # Reusable components
│       │   ├── chat/
│       │   │   ├── ChatMessage.tsx     # Message display
│       │   │   ├── ChatMessage.css
│       │   │   ├── ChatInput.tsx       # Input component
│       │   │   └── ChatInput.css
│       │   │
│       │   └── products/
│       │       ├── ProductCard.tsx     # Product display
│       │       ├── ProductCard.css
│       │       ├── ProductList.tsx     # Product grid
│       │       └── ProductList.css
│       │
│       ├── features/                   # Feature modules
│       │   └── chat/
│       │       ├── ChatContainer.tsx   # Main chat feature
│       │       └── ChatContainer.css
│       │
│       ├── services/                   # API integration
│       │   └── api.ts                  # Backend API calls
│       │
│       ├── types/                      # TypeScript types
│       │   └── index.ts                # Type definitions
│       │
│       ├── utils/                      # Utility functions
│       │   └── format.ts               # Formatting helpers
│       │
│       └── styles/                     # Global styles
│           └── index.css               # CSS variables & globals
│
├── scripts/                            # Utility scripts
│   ├── seed_data.json                  # Sample products (20 items)
│   └── seed_database.py                # Database seeder
│
└── docs/                               # Additional documentation
```

---

## Key Directories Explained

### `/backend/app/graph/` ⭐ **MOST IMPORTANT**

This is where the LangGraph magic happens:

- **`state/`**: Defines the `AgentState` that flows through all nodes
- **`nodes/`**: Individual node functions (pure functions that transform state)
- **`subgraphs/`**: Multi-step workflows for complex operations
- **`tools/`**: Functions the agent can call (decorated with `@tool`)
- **`builders/`**: Assembles the complete graph with routing logic

### `/backend/app/repositories/`

Pure data access layer - no business logic:

- Direct MongoDB operations
- CRUD methods
- Query builders

### `/backend/app/services/`

Business logic orchestration:

- **`gemini_service.py`**: All LLM interactions centralized
- **`chat_service.py`**: Orchestrates graph execution and session management

### `/frontend/src/features/`

Feature-based organization:

- Each feature is self-contained
- `ChatContainer` manages the entire chat experience

---

## File Count Summary

- **Backend Python files**: ~30 modules
- **Frontend TypeScript files**: ~15 modules
- **Total lines of code**: ~5,000+ (with comments)
- **LangGraph nodes**: 15+ nodes
- **Subgraphs**: 3 main workflows
- **Tools**: 6 specialized tools

---

## Important Files for Learning

| Priority | File | What You'll Learn |
|----------|------|-------------------|
| 🔥 | `backend/app/graph/builders/graph_builder.py` | How to assemble a complete LangGraph |
| 🔥 | `backend/app/graph/state/agent_state.py` | State management patterns |
| 🔥 | `backend/app/graph/subgraphs/search_subgraph.py` | Multi-step workflows |
| ⭐ | `backend/app/graph/nodes/route_decision.py` | Deterministic routing |
| ⭐ | `backend/app/graph/tools/search_tools.py` | Tool implementation patterns |
| ⭐ | `backend/app/services/chat_service.py` | Graph invocation & orchestration |
| 💡 | `frontend/src/features/chat/ChatContainer.tsx` | React state management |
| 💡 | `backend/app/services/gemini_service.py` | LLM integration patterns |

---

## Execution Flow

```
1. User types message in React UI
2. Frontend calls /api/v1/chat/message
3. FastAPI endpoint delegates to ChatService
4. ChatService invokes LangGraph
5. Graph executes:
   - classify_intent_node
   - route_by_intent
   - [appropriate subgraph]
   - format_response_node
6. State checkpointed after each node
7. Response returned to frontend
8. UI updates with products/orders
```

---

**This structure is designed for maximum learning value while maintaining production-quality patterns.**
