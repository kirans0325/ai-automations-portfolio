# 🤖 AI Automations & LLM Engineering Portfolio

Welcome to my hands-on portfolio for **AI Automations & LLM Engineering**. This repository contains practical, production-ready projects demonstrating structured AI data extraction, RAG search engines, tool-calling agents, and API microservices.

---

## 📁 Repository Structure

```text
.
├── .gitignore                      # Prevents committing secrets (.env), virtualenvs, & logs
├── README.md                       # Main portfolio overview
├── project1_structured_extractor/  # Project 1: Structured AI Data Extractor & Schema Classifier
│   ├── NOTES.md                    # Detailed learning notes & architecture breakdown
│   ├── pyproject.toml              # Dependencies & package config
│   ├── run.py                      # CLI runner (Offline Mock & Live API modes)
│   ├── samples/                    # Sample unstructured text inputs
│   └── src/                        # Modular extraction engine & Pydantic schemas
```

---

## 🚀 Projects Included

### 1️⃣ [Project 1: Structured AI Data Extractor & Schema Classifier](./project1_structured_extractor/)
- **Goal**: Transform raw, unstructured text (customer tickets, emails) into validated, strongly typed JSON data.
- **Key Tech**: Python, Pydantic v2, Google Gemini API / Mock Local LLM Engine, Rich UI.
- **Notes**: Read [project1_structured_extractor/NOTES.md](./project1_structured_extractor/NOTES.md) for full concepts and code walkthrough.

---

## 🔒 Security Note
This repository uses `.env` for managing API keys locally. `.env` is explicitly ignored in `.gitignore` to ensure credentials are never pushed to GitHub. Use `.env.example` templates provided in each project directory.
