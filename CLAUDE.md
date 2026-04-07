# ShopGraph AI - Architecture Documentation

## Project Overview

**ShopGraph AI** is a production-quality learning project that demonstrates how to build an AI shopping assistant using **LangGraph** for agent orchestration. This project is designed to teach advanced LangGraph concepts through clean, industry-standard code.

### Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: FastAPI (Python 3.11+)
- **Database**: MongoDB
- **LLM Provider**: Google Gemini API
- **Agent Framework**: LangGraph + LangChain (minimal)
- **State Management**: LangGraph Checkpointer + React Context

---

## Learning Objectives

This project teaches the following concepts through practical implementation:

### 1. LangGraph Core Concepts

#### Graph-Based Orchestration
- The agent uses a **directed graph** where each node represents a specific operation
- Edges connect nodes to define the flow of execution
- The graph replaces traditional imperative control flow with declarative state machines

#### Graph State
- **Typed state object** that flows through all nodes
- Contains conversation context, search results, cart state, and more
- State is immutable - nodes return updates that get merged

#### Nodes
- **Pure functions** that take state and return state updates
- Each node has a single responsibility
- Examples: `classify_intent`, `extract_filters`, `format_response`

#### Conditional Routing
- **Router functions** that determine the next node based on current state
- Uses Python code to make routing decisions (not LLM calls)
- Example: Route to search subgraph vs comparison subgraph vs order subgraph

#### Subgraphs
- **Nested graphs** for complex multi-step workflows
- Each subgraph has its own internal state flow
- Examples: SearchSubgraph, ComparisonSubgraph, OrderSubgraph

#### Checkpointer / Memory
- **Persists graph state** between conversations
- Enables conversation resume capability
- Stores conversation history and workflow state
- Uses thread IDs to maintain separate conversation contexts

---

## Architecture Deep Dive

### High-Level System Architecture

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │
       │ HTTP/REST
       │
┌──────▼──────────────────────────────────────────┐
│           React Frontend                        │
│  ┌────────────────────────────────────────┐    │
│  │  Chat Interface  │  Product Cards      │    │
│  │  Cart View       │  Comparison UI      │    │
│  └────────────────────────────────────────┘    │
└──────┬──────────────────────────────────────────┘
       │
       │ REST API
       │
┌──────▼──────────────────────────────────────────┐
│           FastAPI Backend                       │
│  ┌─────────────────────────────────────────┐   │
│  │  API Routes (v1/endpoints)              │   │
│  └──────┬──────────────────────────────────┘   │
│         │                                       │
│  ┌──────▼──────────────────────────────────┐   │
│  │  Services Layer                         │   │
│  │  - ChatService                          │   │
│  │  - GraphExecutionService                │   │
│  └──────┬──────────────┬───────────────────┘   │
│         │              │                        │
│  ┌──────▼──────┐  ┌────▼─────────────────────┐ │
│  │ Repositories │  │  LangGraph Agent        │ │
│  │ - Products   │  │  ┌──────────────────┐   │ │
│  │ - Carts      │  │  │  Main Graph      │   │ │
│  │ - Orders     │  │  │  - Nodes         │   │ │
│  │ - Sessions   │  │  │  - Routers       │   │ │
│  └──────┬───────┘  │  │  - Subgraphs     │   │ │
│         │          │  └────┬─────────────┘   │ │
│         │          │       │                  │ │
│         │          │  ┌────▼─────────────┐   │ │
│         │          │  │  Tools           │   │ │
│         │          │  │  - Search        │   │ │
│         │          │  │  - Compare       │   │ │
│         │          │  │  - Cart/Order    │   │ │
│         │          │  └────┬─────────────┘   │ │
│         │          │       │                  │ │
│         │          │  ┌────▼─────────────┐   │ │
│         │          │  │  Checkpointer    │   │ │
│         │          │  │  (State Memory)  │   │ │
│         │          │  └──────────────────┘   │ │
│         │          └─────────────────────────┘ │
│         │                                       │
│  ┌──────▼──────────────────────────────────┐   │
│  │         MongoDB Database                │   │
│  │  - products                             │   │
│  │  - chat_sessions                        │   │
│  │  - carts                                │   │
│  │  - orders                               │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │      Gemini API (External)              │   │
│  │  - Intent classification                │   │
│  │  - Filter extraction                    │   │
│  │  - Natural language generation          │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Backend Layer Explanation

#### `api/v1/endpoints/`
- **FastAPI route handlers**
- Minimal logic - delegates to services
- Handles request validation and response formatting
- Example: `chat.py` receives messages and calls ChatService

#### `services/`
- **Business logic orchestration**
- Coordinates between repositories and graph execution
- Examples:
  - `ChatService`: Manages chat sessions and graph execution
  - `ProductService`: Business logic for product operations

#### `repositories/`
- **Data access layer**
- Pure CRUD operations on MongoDB
- No business logic
- Examples:
  - `ProductRepository`: Query products from MongoDB
  - `CartRepository`: Manage cart persistence
  - `OrderRepository`: Create and retrieve orders
  - `ChatSessionRepository`: Store conversation history

#### `graph/`
This is the **heart of the LangGraph implementation**:

##### `state/`
- **Type definitions for graph state**
- `AgentState`: Main state that flows through the graph
- Includes: messages, intent, filters, products, cart, errors, etc.

##### `nodes/`
- **Individual node functions**
- Each node is a pure function: `(state) -> state_updates`
- Examples:
  - `classify_intent_node`: Determines user's intent (search/compare/order/chat)
  - `extract_filters_node`: Extracts search parameters from user input
  - `route_node`: Decides which subgraph to execute
  - `format_response_node`: Prepares final response for user

##### `subgraphs/`
- **Nested graph workflows**
- Each subgraph handles a specific complex task:
  - `search_subgraph.py`: Multi-step product search workflow
  - `comparison_subgraph.py`: Product comparison logic
  - `order_subgraph.py`: End-to-end order placement flow

##### `tools/`
- **Executable functions called by the agent**
- Each tool is decorated for LangChain/LangGraph compatibility
- Examples:
  - `search_products_tool`: Query products with filters
  - `compare_products_tool`: Generate comparison data
  - `check_stock_tool`: Validate inventory
  - `add_to_cart_tool`: Add items to cart
  - `place_order_tool`: Create orders

##### `builders/`
- **Graph construction logic**
- `graph_builder.py`: Assembles the complete agent graph
- Connects nodes, adds edges, integrates subgraphs
- Configures checkpointer for state persistence

#### `core/`
- **Configuration and settings**
- Environment variable management
- Constants and enums
- Logging setup

#### `db/`
- **Database connection management**
- MongoDB client initialization
- Index creation

#### `models/`
- **Database models**
- MongoDB document schemas
- ODM (Object-Document Mapping) if using libraries like Beanie

#### `schemas/`
- **Pydantic models for API**
- Request/response DTOs
- Validation schemas

---

## LangGraph Implementation Details

### Main Graph Flow

```
User Input
    ↓
[Update State Node]
    ↓
[Classify Intent Node]
    ↓
[Router Node] ─────→ Intent-based routing
    ├─→ "search" ──→ [Search Subgraph]
    ├─→ "compare" ─→ [Comparison Subgraph]
    ├─→ "order" ───→ [Order Subgraph]
    └─→ "chat" ────→ [General Assistant Node]
    ↓
[Format Response Node]
    ↓
[Save State Node]
    ↓
Response to User
```

### State Management

The `AgentState` is a **TypedDict** that includes:

```python
class AgentState(TypedDict):
    messages: List[BaseMessage]           # Full conversation history
    user_input: str                       # Current user message
    intent: Optional[str]                 # Classified intent
    filters: Optional[Dict]               # Extracted search filters
    products: Optional[List[Product]]     # Current search results
    selected_product_ids: List[str]       # Products selected for comparison/order
    selected_product: Optional[Product]   # Single product for ordering
    comparison_result: Optional[Dict]     # Structured comparison data
    cart_state: Optional[Dict]            # Current cart contents
    order_state: Optional[Dict]           # Order confirmation data
    errors: List[str]                     # Error messages
    thread_id: str                        # Session/conversation identifier
    needs_response: bool                  # Flag for response generation
```

**Key points:**
- State is **immutable** - nodes return partial updates
- State flows through **all nodes in sequence**
- **Checkpointer saves state** after each node execution
- Thread ID enables **conversation context isolation**

### Subgraph Example: Search Subgraph

```
[Extract Filters] ─→ Uses Gemini to parse filters from user input
       ↓
[Call Search Tool] ─→ Executes search against MongoDB
       ↓
[Normalize Results] ─→ Formats products into standard structure
       ↓
[Update State] ─→ Stores products in state.products
```

**Why a subgraph?**
- Encapsulates the **multi-step search logic**
- Reusable across different entry points
- **Isolates complexity** from main graph
- Enables easier testing and debugging

### Routing Logic

Routing is done using **Python functions**, not LLM calls:

```python
def route_by_intent(state: AgentState) -> str:
    """
    Deterministic routing based on classified intent.
    Returns the name of the next node or subgraph.
    """
    intent = state.get("intent")

    if intent == "search":
        return "search_subgraph"
    elif intent == "compare":
        return "comparison_subgraph"
    elif intent == "order":
        return "order_subgraph"
    else:
        return "general_chat_node"
```

**Why Python routing?**
- **Faster** than LLM calls
- **Deterministic** and predictable
- **Cost-effective**
- Easier to debug and test

### Checkpointer and Memory

The **checkpointer persists graph state** to enable:

1. **Conversation continuity**: Resume chats after disconnection
2. **Multi-turn interactions**: Remember search results across turns
3. **Workflow state**: Track progress in multi-step flows (e.g., ordering)

**Implementation:**
```python
from langgraph.checkpoint.memory import MemorySaver

# For development
checkpointer = MemorySaver()

# For production
# checkpointer = MongoDBCheckpointer(connection_string)

graph = builder.compile(checkpointer=checkpointer)
```

**What gets checkpointed?**
- Complete `AgentState` after each node execution
- Conversation messages
- Current search results
- Selected products
- Cart state

**How it helps:**
```
User: "Find gaming laptops"
  → State saved: products = [list of laptops]

User: "Compare the first two"
  → State loaded: products still available
  → No need to re-search
```

---

## Tool Design

### Tool Structure

Each tool follows this pattern:

```python
from langchain.tools import tool
from typing import Dict, List, Optional

@tool
def search_products_tool(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None
) -> Dict:
    """
    Search for products based on filters.

    Args:
        category: Product category (e.g., "laptop", "phone")
        brand: Brand name filter
        min_price: Minimum price filter
        max_price: Maximum price filter
        min_rating: Minimum rating filter

    Returns:
        Dict with 'success', 'products', and optional 'error'
    """
    # Tool implementation
    pass
```

**Key principles:**
- **Strong typing** with type hints
- **Clear docstrings** for LLM to understand usage
- **Standardized response format** (success/error pattern)
- **Single responsibility** per tool
- **No direct state access** - tools are pure functions

### Tool Catalog

1. **search_products_tool**: Query products by filters
2. **filter_products_tool**: Refine existing results
3. **compare_products_tool**: Generate product comparisons
4. **check_stock_tool**: Validate product availability
5. **add_to_cart_tool**: Add product to user's cart
6. **place_order_tool**: Create order record

---

## Frontend Architecture

### Component Structure

```
src/
├── components/          # Reusable UI components
│   ├── chat/           # Chat-specific components
│   ├── products/       # Product display components
│   ├── cart/           # Cart UI components
│   └── common/         # Shared components (buttons, inputs)
├── features/           # Feature-based modules
│   ├── chat/           # Chat feature logic
│   ├── products/       # Product feature logic
│   └── cart/           # Cart feature logic
├── hooks/              # Custom React hooks
├── services/           # API integration services
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
└── pages/              # Page components
```

### State Management

Uses **React Context** for:
- Chat messages
- Current products
- Cart state
- User session

**Why Context over Redux?**
- Simpler for this use case
- Less boilerplate
- Sufficient for moderate state complexity

### API Integration

All backend communication goes through **service layers**:

```typescript
// services/chatService.ts
export async function sendMessage(message: string, threadId: string) {
  const response = await fetch('/api/v1/chat/message', {
    method: 'POST',
    body: JSON.stringify({ message, thread_id: threadId })
  });
  return response.json();
}
```

---

## Data Flow Example

Let's trace a complete user interaction:

### User: "Find gaming laptops under $1500"

#### Frontend:
1. User types message in chat input
2. React calls `chatService.sendMessage()`
3. POST to `/api/v1/chat/message`

#### Backend API:
4. `chat.py` endpoint receives request
5. Validates request with Pydantic schema
6. Calls `ChatService.process_message()`

#### Service Layer:
7. `ChatService` retrieves or creates chat session
8. Calls `GraphExecutionService.execute_graph()`

#### LangGraph Execution:
9. **Update State Node**: Adds user message to state
10. **Classify Intent Node**: Calls Gemini → intent = "search"
11. **Router Node**: Routes to `search_subgraph`
12. **Search Subgraph**:
    - **Extract Filters Node**: Calls Gemini → {category: "laptop", max_price: 1500, tags: ["gaming"]}
    - **Search Tool Node**: Calls `search_products_tool`
    - **Search Tool**: Calls `ProductRepository.search()`
    - **Repository**: Queries MongoDB
    - **Tool returns**: List of products
    - **Normalize Node**: Formats results
13. **Format Response Node**: Generates user-friendly message
14. **Checkpointer**: Saves complete state

#### Service Layer:
15. `ChatService` stores message in session
16. Returns response with products

#### Frontend:
17. React receives response
18. Updates chat messages
19. Renders product cards
20. User sees results

---

## Key Design Decisions

### Why LangGraph over simple LLM calls?

1. **Stateful workflows**: Need to remember search results, cart state
2. **Complex routing**: Different flows for search/compare/order
3. **Tool orchestration**: Multiple tools need coordination
4. **Resumable conversations**: Checkpointer enables this
5. **Testability**: Each node can be tested independently

### Why separate subgraphs?

1. **Modularity**: Each workflow is self-contained
2. **Reusability**: Subgraphs can be called from multiple entry points
3. **Clarity**: Easier to understand complex flows
4. **Maintainability**: Changes to one flow don't affect others

### When to use Gemini vs Python?

**Use Gemini for:**
- Intent classification from natural language
- Extracting filters from free-form text
- Generating natural comparison explanations
- General conversational responses

**Use Python for:**
- Routing decisions (deterministic)
- Data formatting
- Validation logic
- Database operations

### Why FastAPI?

1. **Modern async support**: Handles concurrent requests efficiently
2. **Automatic API docs**: Built-in Swagger UI
3. **Type safety**: Pydantic integration
4. **Performance**: Fast compared to Flask/Django

### Why MongoDB?

1. **Flexible schema**: Easy to iterate on product structure
2. **JSON-native**: Natural fit for Python dicts
3. **Good for learning**: Simple to set up and use
4. **Realistic**: Common choice for e-commerce

---

## Development Guidelines

### Adding a New Node

1. Create node function in `backend/app/graph/nodes/`
2. Define input/output behavior with state
3. Add node to graph in `graph_builder.py`
4. Connect with appropriate edges
5. Test node in isolation

### Adding a New Tool

1. Create tool in `backend/app/graph/tools/`
2. Use `@tool` decorator
3. Add type hints and docstring
4. Implement business logic
5. Return standardized response format
6. Register tool in graph builder

### Adding a New Subgraph

1. Create subgraph file in `backend/app/graph/subgraphs/`
2. Define subgraph state (if different from main state)
3. Create subgraph nodes
4. Build subgraph with `StateGraph`
5. Integrate into main graph
6. Add routing logic

---

## Testing Strategy

### Unit Tests
- Test individual nodes with mock state
- Test tools with mock repositories
- Test repositories with test database

### Integration Tests
- Test complete graph flows
- Test API endpoints
- Test subgraph integration

### Example Node Test
```python
def test_classify_intent_node():
    state = {
        "user_input": "Find laptops",
        "messages": []
    }
    result = classify_intent_node(state)
    assert result["intent"] == "search"
```

---

## Environment Setup

### Backend Environment Variables
```
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=shopgraph_ai
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-pro
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend Environment Variables
```
VITE_API_BASE_URL=http://localhost:8000
```

---

## Production Considerations

### Current Implementation (Development)
- In-memory checkpointer
- Basic error handling
- Console logging

### Production Enhancements Needed
1. **Persistent checkpointer**: MongoDB/Redis-based
2. **Authentication**: User authentication and session management
3. **Rate limiting**: Prevent API abuse
4. **Monitoring**: Logging, metrics, tracing
5. **Caching**: Redis for frequent queries
6. **Error tracking**: Sentry or similar
7. **Database indexes**: Optimize MongoDB queries
8. **Load balancing**: Handle multiple instances
9. **CI/CD**: Automated testing and deployment
10. **Security**: Input sanitization, CORS, HTTPS

---

## Learning Path

### For Beginners
1. Start with `README.md` for setup
2. Run the app and test basic flows
3. Read this file to understand architecture
4. Explore `graph_builder.py` to see graph structure
5. Study one subgraph in detail
6. Modify a node to see effects

### For Intermediate
1. Add a new intent and routing path
2. Create a new tool
3. Build a custom subgraph (e.g., recommendations)
4. Implement additional filters
5. Add error handling improvements

### For Advanced
1. Implement persistent checkpointer
2. Add streaming responses
3. Optimize graph execution
4. Add A/B testing for different prompts
5. Implement graph visualization
6. Build custom LangGraph inspector

---

## Common Patterns

### Pattern: Intent-Based Routing
```python
# Classify intent → Route → Execute specialized flow
classify_intent_node → router_node → subgraph_by_intent
```

### Pattern: Tool Calling with Fallback
```python
# Try tool → Handle error → Fallback to LLM
try_tool_node → error_check_node → fallback_node
```

### Pattern: State Accumulation
```python
# Multiple nodes add to state progressively
extract_node (adds filters) →
search_node (adds products) →
format_node (adds response)
```

### Pattern: Conditional Subgraph
```python
# Only enter subgraph if condition met
def should_enter_comparison(state):
    return len(state.get("selected_product_ids", [])) >= 2
```

---

## Glossary

- **Node**: A function in the graph that processes state
- **Edge**: Connection between nodes defining execution order
- **State**: Data object that flows through the graph
- **Subgraph**: Nested graph for complex workflows
- **Checkpointer**: Mechanism for persisting state
- **Tool**: External function callable by the agent
- **Intent**: Classified purpose of user's message
- **Thread**: Isolated conversation context
- **Router**: Node that determines next execution path

---

## Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Best Practices](https://www.mongodb.com/docs/manual/administration/production-notes/)
- [React TypeScript Guide](https://react-typescript-cheatsheet.netlify.app/)

---

## Project Stats

- **Backend Files**: ~30 Python modules
- **Frontend Files**: ~25 TypeScript/React files
- **LangGraph Nodes**: ~15 nodes
- **Subgraphs**: 3 main subgraphs
- **Tools**: 6 specialized tools
- **Database Collections**: 4 collections
- **API Endpoints**: ~8 endpoints

---

## Conclusion

This project demonstrates **production-quality LangGraph implementation** with:

✅ Clear separation of concerns
✅ Modular, testable architecture
✅ Educational code comments
✅ Realistic feature set
✅ Industry-standard patterns
✅ Scalable structure

Use this codebase to **learn LangGraph deeply**, understand **agentic workflows**, and build **stateful AI applications**.

Happy learning! 🚀
