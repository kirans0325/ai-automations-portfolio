# 🎓 Project 2 Notes: Retrieval-Augmented Generation (RAG) Document QA Bot

## 1. 💡 What is RAG and Why is it the #1 Pattern in AI Engineering?

Large Language Models (LLMs) like GPT-4 or Gemini are trained on public internet data up to a specific cutoff date. However:
- **LLMs don't know your private files**: They have zero knowledge of your company's internal PDFs, HR policies, private codebases, or customer documents.
- **LLMs Hallucinate**: If you ask an LLM about your company's private policy, it will make up plausible-sounding but completely false answers.

### The Solution: Retrieval-Augmented Generation (RAG)
Instead of re-training or fine-tuning the LLM (which is extremely expensive), **RAG** acts like an **"Open-Book Exam"** for the AI:
1. **Search Phase (Retrieval)**: When the user asks a question, the system searches a local **Vector Database** for the top 2-3 most relevant snippets from your documents.
2. **Answer Phase (Generation)**: The system passes those exact document snippets into the LLM's prompt and instructs it:  
   *"Answer the user's question STRICTLY using these provided document snippets."*

---

## 2. 🧩 The 4 Core Steps of a RAG Pipeline

```text
[Raw Documents] ➔ 1. Chunking ➔ 2. Embeddings ➔ 3. Vector Search ➔ 4. Grounded Prompting ➔ [Accurate Answer]
```

### Step 1: Text Chunking (`src/chunker.py`)
- **Why chunk?** A 50-page PDF is too big to convert into a single vector embedding. Large documents get diluted.
- **Sliding Window Chunking**: We break text into small pieces (e.g., 100 words per chunk) with a 20-word **overlap** so sentences split across boundaries aren't lost.

### Step 2: Vector Embedding & Storage (`src/vector_store.py`)
- **What is an Embedding?** A mathematical vector array (`[0.12, -0.45, 0.88, ...]`) that captures the *semantic meaning* of text.
- **Cosine Similarity**: A formula that measures the angle between two vectors to see how close their meanings are:
  $$\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
  - Score of `1.0` = Identical meaning.
  - Score of `0.0` = Completely unrelated.

### Step 3: Semantic Retrieval (`src/rag_engine.py`)
- When a user asks: *"What is the remote work equipment stipend?"*, the vector engine calculates similarity scores across all document chunks and picks the top matches.

### Step 4: Grounded Prompting
We construct a grounded prompt:
```text
KNOWLEDGE BASE CONTEXT:
--- [Source: company_policy.txt] ---
Each remote employee is entitled to a one-time remote home office setup stipend of $1,200 USD.

USER QUESTION:
What is the remote work equipment setup stipend amount?

INSTRUCTION:
Answer strictly based on the context above.
```

---

## 3. 🏗 Codebase Architecture

```text
project2_rag_document_bot/
├── docs/                     # Knowledge base documents (.txt / .md / .pdf)
│   ├── company_policy.txt
│   ├── product_guide.txt
│   └── api_troubleshooting.txt
├── src/
│   ├── chunker.py            # Sliding window document text splitter
│   ├── vector_store.py       # In-memory vector database & cosine similarity engine
│   └── rag_engine.py         # Grounded prompt builder & QA orchestrator
├── run.py                    # Interactive CLI Q&A runner
└── NOTES.md                  # Detailed learning guide
```

---

## 4. 🚀 How to Run & Test Project 2 Locally

### Step 1: Install Dependencies
From the workspace root (`e:\code\ai-ml-projects\abc-ai`), run:
```bash
uv pip install -e project2_rag_document_bot
```

### Step 2: Run the RAG Bot
```bash
.venv\Scripts\python project2_rag_document_bot/run.py
```

### Step 3: What You Will See
The CLI will index all documents in `docs/`, calculate similarity rankings for user questions, display retrieved source chunks with relevance scores (`0.8521`), and output grounded answers!

---

## 🐙 Pushing to GitHub
```bash
git add .
git commit -m "feat: implement project 2 RAG document QA bot with vector store & notes"
git push origin main
```
