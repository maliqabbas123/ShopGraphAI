# ShopGraphAI

An AI-powered shopping assistant that handles natural language product search, comparison, and order placement through a multi-turn conversational interface. Built to explore LangGraph stateful agent patterns with a full-stack FastAPI + React setup.

## Tech Stack

**Backend:** FastAPI, LangGraph, LangChain, Google Gemini API, Motor (async MongoDB)

**Frontend:** React 18, TypeScript, Vite, Tailwind CSS

**Database:** MongoDB

## Architecture

Each user message flows through a LangGraph agent:

```
User Message
     |
[classify_intent]   <-- Gemini classifies intent
     |
[route_by_intent]   <-- deterministic Python routing
     |
     +-- search_subgraph      (product search + filter)
     +-- comparison_subgraph  (side-by-side comparison)
     +-- order_subgraph       (cart + checkout)
     +-- general_chat         (freeform conversation)
     |
[format_response]
     |
Response
```

A `MemorySaver` checkpointer persists the full `AgentState` between turns, so search results stay available for follow-up comparisons or ordering without re-querying.

## Project Structure

```
backend/
  app/
    api/v1/endpoints/   # FastAPI route handlers
    graph/
      builders/         # graph_builder.py — assembles the full graph
      nodes/            # classify_intent, general_chat, format_response nodes
      subgraphs/        # search, comparison, order subgraphs
      tools/            # search_tools, comparison_tools, order_tools
      state/            # AgentState TypedDict
    models/             # MongoDB document models
    repositories/       # DB access layer (product, order, cart, chat)
    services/           # chat_service, gemini_service
    db/                 # MongoDB connection

frontend/
  src/
    components/         # ChatMessage, ChatInput, ProductCard, ProductList
    features/chat/      # ChatContainer
    services/           # api.ts HTTP client
    types/              # TypeScript interfaces

scripts/
  seed_database.py      # Seeds 20 sample products into MongoDB
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB running locally
- Google Gemini API key

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` — the only required change is your API key:

```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=shopgraph_ai
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Seed the database and start:

```bash
python scripts/seed_database.py
uvicorn app.main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# App: http://localhost:5173
```

The frontend defaults to `http://localhost:8000` for the backend. Override with `VITE_API_BASE_URL` in a `.env` file if needed.

## Example Prompts

```
"Find gaming laptops under $1500"
"Compare the top 3 options"
"Only show Samsung"
"Order the cheapest one"
```
