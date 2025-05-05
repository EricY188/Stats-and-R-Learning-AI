
# 📊 Stats‑and‑R‑Learning‑AI

**Stats‑and‑R‑Learning‑AI** is an open‑source AI tutor that

* answers statistics questions in plain English,  
* generates and _runs_ tidy R code on demand,  
* cites authoritative sources (CRAN docs, “R for Data Science”, lecture notes), and  
* recommends the next concept you should learn.

Under the hood it uses a **retrieval‑augmented generation** (RAG) workflow powered by LangChain agents, a FAISS vector database, and GPT‑class LLMs (OpenAI _or_ Anthropic).

---

## ✨ Key Features

| Step | Agent / Tool | What it does |
|------|--------------|--------------|
| 1  Question Validator | LLM classifier prompt | Blocks off‑topic queries (“Write me a poem”) |
| 2  Context Retriever | FAISS + Hugging Face embeddings | Pulls best‑matching doc chunks |
| 3  Teaching Agent | GPT‑4o‑mini / Claude Haiku | Crafts an explanation & R snippet (```r … ```) |
| 4  Next‑Lesson Agent | Light prompt‑based | Suggests a follow‑up topic & reading link |
| 5  Optional R Exec | Sandbox via `Rscript` | Executes the code and returns output / plot |

---

## 🏗️ Architecture at a Glance

```
┌─────────────┐   POST /api/query   ┌────────────────────┐
│  React UI   ├────────────────────►│ FastAPI Backend    │
└─────────────┘                    │  (LangChain agents) │
        ▲                          └────────┬────────────┘
        │                                   │
        │ GET /api/query                   ▼
        │                          ┌─────────────────┐
        │                          │  FAISS Vector   │
        │                          │   Database      │
        │                          └─────────────────┘
        │                                   │
        │               ┌───────────────┐   │
        └──────────────►│  R sandbox    │◄──┘
                        └───────────────┘
```

* **Backend** – FastAPI + LangChain LCEL agents  
* **Vector DB** – local FAISS index (`backend/faiss_index/`)  
* **Front‑end** – React + Chakra UI (mobile friendly)  
* **Optional** – server‑side R execution (requires R ≥ 4.x)

---

## 📦 Directory Layout

```
Stats‑and‑R‑Learning‑AI
│
├─ backend/
│  ├─ agents/              # validator / retriever / teaching / next‑step
│  ├─ tools/               # r_exec_tool.py
│  ├─ scripts/             # build_faiss.py
│  ├─ data/                # raw markdown docs (R4DS, CRAN man pages…)
│  ├─ faiss_index/         # generated vector store (git‑ignored)
│  └─ manage.py            # FastAPI entry‑point
│
├─ ai‑tutor‑frontend/      # React app
│
├─ requirements.txt        # Python deps
├─ .env.example            # env‑var template
└─ README.md               # <— you’re reading it
```

---

## 🚀 Quick Start (Local)

### 1  Clone & Python env

```bash
git clone https://github.com/<your‑handle>/Stats-and-R-Learning-AI.git
cd Stats-and-R-Learning-AI
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2  Fill in API keys

```bash
cp .env.example .env
# edit .env with OPENAI_API_KEY or ANTHROPIC_API_KEY
```

### 3  Build the vector database (first run only)

```bash
python backend/scripts/build_faiss.py
```

> Put additional Markdown or plain‑text references into `backend/data/` and rerun the script any time.

### 4  ( Optional ) Install R packages

Only needed if you want server‑side code execution.

```r
install.packages(c("tidyverse", "broom", "palmerpenguins"))
```

### 5  Run the backend

```bash
uvicorn backend.manage:app --reload
```

### 6  Run the front‑end

```bash
cd ai-tutor-frontend
npm install
npm start
```

Open <http://localhost:3000> and ask:

> _“Fit a logistic regression in R using `glm()` and interpret the coefficients.”_

---

## 🖥️ API Reference

| Route | Method | Body | Description |
|-------|--------|------|-------------|
| `/api/query/` | POST | `{ "question": "…", "run_code": true/false }` | Returns JSON with: `answer`, `citations[]`, `next_step`, `r_output` (stdout / stderr / plot hex) |

---

## 🗃️ Bundled Data Sources

* **R for Data Science** (2e, CC BY‑NC‑SA) – converted to Markdown  
* Selected CRAN man pages for `stats`, `dplyr`, `ggplot2`, …  
* Coursera “Statistics with R” lecture notes (public domain)  
* Popular StackOverflow Q&A (CC BY‑SA 4.0)

> All third‑party content retains the original license.  
> You can freely add or remove material to match your curriculum.

---

## ⚙️ Configuration

| Env var | Default | Description |
|---------|---------|-------------|
| `OPENAI_API_KEY` | – | Needed if `"MODEL_PROVIDER" = openai` |
| `ANTHROPIC_API_KEY` | – | Needed if `"MODEL_PROVIDER" = anthropic` |
| `MODEL_PROVIDER` | `openai` | `openai` or `anthropic` |
| `PORT` | 8000 | Overridden by Uvicorn option `--port` |

---

## 🛡️ Security & Cost Controls

* **Rate‑limit**: not yet—add `slowapi` or your favourite middleware.  
* **LLM cache**: enable LangChain in‑memory or SQLite cache to cut tokens.  
* **R sandbox**: current helper runs via `Rscript` + temp dir; for production isolate in Docker with `seccomp` or `firejail`.

---

## 🐳 Docker (optional)

```dockerfile
# quick‑and‑dirty multi‑stage example
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS builder
COPY backend/ backend/
COPY .env.example ./
RUN python backend/scripts/build_faiss.py

FROM base
COPY --from=builder /app /app
EXPOSE 8000
CMD ["uvicorn", "backend.manage:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build & run:

```bash
docker build -t stats-r-ai .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY stats-r-ai
```

---

## 👩‍💻 Contributing

Pull requests welcome!  If you:

1. spot a 🐛,  
2. want to add a new agent/tool (e.g. `ggplot_exec_tool.py`), or  
3. have curriculum docs you can legally share,

please open an issue or PR.

### Dev tips

```bash
# lint + type‑check
pip install ruff mypy
ruff backend
mypy backend
```

---

## 📜 License

**MIT**.  Do anything you want, but keep the copyright notice and give attribution to third‑party docs you redistribute.

---

## 🙏 Acknowledgements

* Hadley Wickham & Garrett Grolemund – *R for Data Science*  
* CRAN & R‑core for open documentation  
* LangChain, FAISS, OpenAI, Anthropic, Chakra UI

Happy learning & coding! 💙
