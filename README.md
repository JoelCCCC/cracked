# ⚡ CRACKED

A personal software engineering mastery platform designed to take you from fundamental syntax to deep engineering expertise across **6 core disciplines**:

1. **Coding Foundations** (Data structures, control flow, functions, error handling, performance habits)
2. **Algorithms & Data Structures** (Two pointers, sliding window, recursion, dynamic programming, graphs)
3. **Web Development** (HTTP semantics, browser rendering, REST/GraphQL APIs, concurrency, caching)
4. **Database Design** (Relational modeling, normalization, indexing strategies, transactions & ACID)
5. **DevOps & Infrastructure** (Linux primitives, Docker containerization, CI/CD pipelines, Kubernetes)
6. **AI Engineering** (Tokenization, embeddings, vector search, RAG pipelines, prompt engineering)

---

## 🏗 Architecture

- **Frontend (`/frontend`)**: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4, Lucide React icons, and custom interactive Code Editor.
- **Backend (`/backend`)**: Python 3 / Django 5.1, Django REST Framework, SimpleJWT authentication, and an isolated code execution engine for test validation.
- **Database**: PostgreSQL 17 running via Docker Compose (`cracked-db` on port `5434`).

---

## 🚀 Quick Start

### 1. Start the PostgreSQL Database
```bash
docker compose up -d
```

### 2. Setup and Run the Django Backend
```bash
cd backend
source .venv/bin/activate

# Apply migrations
python manage.py migrate

# Seed the 6 tracks, 18 levels, and 72 challenges
python manage.py seed_curriculum

# Run automated tests
python manage.py test

# Start the API server on http://localhost:8000
python manage.py runserver 0.0.0.0:8000
```

### 3. Setup and Run the Next.js Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start the dev server on http://localhost:3000
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🎯 Personal Mastery Features

- **Seamless Local Workspace**: Automatically authenticates into your personal profile (`lavid`) with zero login prompts on startup.
- **Sequential Unlocking**:
  - Completing **Level 1** unlocks **Level 2**, and completing Level 2 unlocks Level 3.
  - Accumulating total XP unlocks higher-tier disciplines (Coding $\rightarrow$ Algorithms $\rightarrow$ Web $\rightarrow$ DB $\rightarrow$ DevOps $\rightarrow$ AI).
- **Personal Solution Vault (`/history`)**:
  - Automatically archives every working solution and code implementation you submit.
  - Searchable and filterable by discipline and concept.
- **Interactive Level Arena (`/levels/[id]`)**:
  - **Theory Lessons**: Markdown lessons with practical engineering rules of thumb.
  - **Scored Challenges**:
    - **Code Challenges**: In-browser code editor with automated unit test runner.
    - **Multiple Choice (MCQ)**: Instant concept validation.
    - **Multi-select**: Multiple-answer questions.
    - **Short Answer**: Concise syntax and command prompt verification.
  - **Practice Reset**: Button to reset progress on any individual level if you want to practice it again.
- **Rank Ladder**:
  - Personal rank advancement: Script Kiddie (0 XP) $\rightarrow$ Junior (250 XP) $\rightarrow$ Builder (750 XP) $\rightarrow$ Engineer (1500 XP) $\rightarrow$ Senior (3000 XP) $\rightarrow$ Architect (5000 XP) $\rightarrow$ **Cracked** (8000+ XP).
  - Daily streak tracker to maintain consistent coding habits.
