# 🎓 Project 1 Notes: Structured AI Data Extractor & Schema Classifier

## 1. 💡 Core AI Engineering Concept: Why Structured Outputs Matter
In real-world software engineering, sending a prompt to an LLM and receiving unstructured Markdown or free text is dangerous for production systems. 

### The Problem with Unstructured LLM Responses:
- **Inconsistent Keys**: The LLM might return `"customer_name"` in one request and `"client"` in the next.
- **Parsing Errors**: Free-form text cannot be directly stored in SQL databases or passed to internal APIs.
- **Hallucinated Datatypes**: The model might return a string `"100 dollars"` when your code expects an integer `100`.

### The Solution: Pydantic Schema Enforcement
By pairing an LLM with **Pydantic schemas**:
1. **Guaranteed Schema**: The LLM output is constrained to adhere strictly to your data structure.
2. **Type Safety**: Enums, Integers, Datetimes, and Lists are automatically type-validated before your code touches them.
3. **Production Reliability**: If validation fails, Pydantic raises clear errors so your application can retry cleanly.

---

## 2. 🏗 Architecture & Code Walkthrough

```text
project1_structured_extractor/
├── pyproject.toml       # Virtual env & package metadata
├── .env.example         # Template for API keys (NEVER commit real .env to GitHub)
├── NOTES.md             # This educational guide
├── run.py               # Interactive CLI runner with rich output
├── samples/             # Sample raw support ticket text files
└── src/
    ├── models.py        # Pydantic schemas (Enums, ActionItems, TicketAnalysis)
    ├── mock_llm.py      # Offline rule-assisted parser for instant keyless testing
    └── extractor.py     # Main engine (supports Live Gemini API & Offline Mock)
```

### Deep Dive: `src/models.py`
We define our data schema using Pydantic `BaseModel` and `Enum`:

```python
class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    FEATURE_REQUEST = "feature_request"
    ACCOUNT_ACCESS = "account_access"
    OTHER = "other"

class SupportTicketAnalysis(BaseModel):
    ticket_summary: str = Field(description="Concise 1-2 sentence summary")
    category: TicketCategory = Field(description="Primary category")
    priority: PriorityLevel = Field(description="Urgency/priority level")
    customer_name: Optional[str] = Field(default=None)
    action_items: List[ActionItem] = Field(default_factory=list)
```
- `Enum`: Forces the LLM to choose **only** from pre-approved category values.
- `Field(description=...)`: Provides explicit hints to the LLM during structured output generation so it knows what to extract.

---

## 3. 🚀 How to Run & Test This Project

### Step 1: Install Dependencies
From the workspace root (`e:\code\ai-ml-projects\abc-ai`), run:
```bash
uv venv
uv pip install -e project1_structured_extractor
```

### Step 2: Run in Offline Mock Mode (No API Key Required)
```bash
python project1_structured_extractor/run.py
```
This will parse all sample tickets in `samples/` using the local mock engine and render colorized Pydantic tables.

### Step 3: Run with Live Cloud Gemini API (Optional)
1. Create a `.env` file inside `project1_structured_extractor/`:
   ```bash
   cp project1_structured_extractor/.env.example project1_structured_extractor/.env
   ```
2. Open `project1_structured_extractor/.env` and add your key:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   ```
3. Run `python project1_structured_extractor/run.py` again. It will automatically detect your key and run live LLM extraction!

---

## 🐙 Smart GitHub Push Guide

To keep your repository clean, modular, and secure:

### 1. Verify Secret Security
Check that `.gitignore` contains `.env` so your API key is **never** committed:
```bash
git status
```
Ensure `.env` does **NOT** show up under untracked files.

### 2. Initialize & Commit Locally
```bash
git init
git add .
git commit -m "feat: implement project 1 structured AI data extractor with Pydantic & learning notes"
```

### 3. Push to GitHub
1. Create a new public/private repository on [GitHub](https://github.com/new) named `abc-ai` (or `ai-automations-portfolio`).
2. Link your local repo and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```
