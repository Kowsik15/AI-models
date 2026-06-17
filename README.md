# AI-models

# Transformers — Resume Analyser

An AI-powered **Resume vs. Job Description matcher** that scores how well a candidate's resume aligns with a target job, extracts matched skills, and gives recruiter-style feedback. Built with **Flask**, **pdfplumber**, and (in the notebook version) **HuggingFace Transformer embeddings** for semantic similarity.

> Part of the [AI-models](https://github.com/Kowsik15/AI-models) repository.

---

## 📁 Folder Structure

```
Transformers/
├── Resume Analyser/
│   └── Resume Analyse V1/                 # Notebook prototype + minimal app
│       ├── Resume Job Analysis.ipynb      # Transformer-based similarity experiments
│       ├── app.py                         # Minimal Flask entry
│       ├── templates/index.html
│       └── static/style.css
└── Resume Analyser Deploy/                # Production-style Flask app
    ├── app.py                             # Flask server + scoring pipeline
    ├── templates/
    │   └── index.html                     # Upload resume + paste JD
    └── static/
        └── style.css
```

---

## ✨ Features

- 📄 Upload a resume PDF and paste any job description
- 🔍 Automatic **skill extraction** from both resume and JD
- 📊 **Similarity score (0–100%)** based on skill overlap (deploy version) or **transformer embeddings** (notebook version)
- 🧑‍💼 **Recruiter-style feedback**: *Excellent / Good / Moderate / Low Match*
- 🌐 Clean Flask web UI
- 🧪 Jupyter notebook for swapping in any HuggingFace model

---

## 🏗️ How It Works

```
Resume PDF ──► pdfplumber ──► text
                                 │
Job Description (text) ──────────┤
                                 ▼
                       Skill Extraction
                                 │
                ┌────────────────┴───────────────┐
                ▼                                ▼
   Skill-overlap score (deploy)    Transformer embeddings (notebook)
                │                                │
                └────────────────┬───────────────┘
                                 ▼
                       Score + Recruiter Feedback
```

### Skill vocabulary (deploy version)

`python, sql, tableau, power bi, excel, machine learning, deep learning,
tensorflow, keras, pandas, numpy, scikit-learn, nlp, rag, transformers,
aws, azure, docker, git, flask`

Extend the `SKILLS` list in `app.py` to fit your domain.

### Scoring (deploy version)

```
score = |resume_skills ∩ jd_skills| / |jd_skills| * 100
```

| Score   | Feedback        |
|---------|-----------------|
| ≥ 85    | Excellent Match |
| 70–84   | Good Match      |
| 50–69   | Moderate Match  |
| < 50    | Low Match       |

The notebook (`Resume Job Analysis.ipynb`) replaces this with **sentence-transformer embeddings + cosine similarity** for a semantic match.

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/Kowsik15/AI-models.git
cd AI-models/Transformers/Resume\ Analyser\ Deploy
```

### 2. Install dependencies

```bash
pip install -r ../../requirements.txt
pip install flask pdfplumber
```

### 3. Run the app

```bash
python app.py
```

Open <http://127.0.0.1:5000>, upload a resume PDF, paste a job description, and submit to see the match score and feedback.

### 4. (Optional) Explore the notebook

```bash
jupyter lab "../Resume Analyser/Resume Analyse V1/Resume Job Analysis.ipynb"
```

The notebook uses HuggingFace `transformers` / `sentence-transformers` for embedding-based similarity — a more robust replacement for keyword matching.

---

## 🧩 Key Components

| Component | Purpose |
|-----------|---------|
| `pdfplumber` | Extracts raw text from resume PDFs |
| `extract_skills()` | Keyword-based skill detection |
| `calculate_similarity()` | Overlap score (deploy) / embedding cosine (notebook) |
| `recruiter_feedback()` | Maps score → human-readable verdict |
| Flask + Jinja2 | Web UI |

---

## 🔧 Customising

- **Add skills**: edit the `SKILLS` list in `app.py`.
- **Switch to semantic scoring**: replace `calculate_similarity` with a sentence-transformer embedding + cosine similarity (see the notebook).
- **Persist results**: wire in a database (SQLite / Postgres) to track applicants over time.

---

## 📜 License

MIT — see [LICENSE](../LICENSE).


# RAG — Retrieval Augmented Generation

A PDF-aware question-answering system built with **LangChain**, **FAISS**, **HuggingFace embeddings**, and a **local Llama 3 LLM served via Ollama**. Upload a PDF, ask questions in natural language, and get answers grounded in the document.

> Part of the [AI-models](https://github.com/Kowsik15/AI-models) repository.

---

## 📁 Folder Structure

```
RAG/
├── RAG V1/                  # Notebook prototype
│   └── RAG.ipynb            # End-to-end RAG pipeline (experiments)
└── Rag Deploy/              # Flask web app
    ├── app.py               # Flask server + RAG pipeline
    ├── templates/
    │   └── index.html       # Upload + chat UI
    ├── static/
    │   └── style.css        # Styles
    └── upload/              # Uploaded PDFs (sample included)
```

---

## ✨ Features

- 📄 Upload any PDF and index it on the fly
- 🔎 Semantic search over document chunks using **FAISS**
- 🧠 Embeddings via `sentence-transformers/all-MiniLM-L6-v2`
- 💬 Answers generated by a **local Llama 3** model through **Ollama** (no API keys, fully offline)
- 🌐 Lightweight **Flask** web interface
- 🧪 Reproducible Jupyter notebook (`RAG V1/RAG.ipynb`) for experimentation

---

## 🏗️ How It Works

```
PDF ──► PyPDFLoader ──► RecursiveCharacterTextSplitter
                              │ (chunks of 1000, overlap 100)
                              ▼
                    HuggingFace Embeddings
                              │
                              ▼
                         FAISS Vector DB
                              │
   user query ──► similarity_search (k=5) ──► context
                              │
                              ▼
                   Prompt + context ──► Llama 3 (Ollama) ──► Answer
```

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/Kowsik15/AI-models.git
cd AI-models/RAG/Rag\ Deploy
```

### 2. Install Python dependencies

```bash
pip install -r ../../requirements.txt
pip install flask langchain langchain-community langchain-ollama \
            faiss-cpu sentence-transformers pypdf
```

### 3. Install & start Ollama with Llama 3

[Download Ollama](https://ollama.com/download), then:

```bash
ollama pull llama3
ollama serve
```

### 4. Run the Flask app

```bash
python app.py
```

Open <http://127.0.0.1:5000> in your browser, upload a PDF, and start asking questions.

### 5. (Optional) Explore the notebook

```bash
jupyter lab "../RAG V1/RAG.ipynb"
```

---

## 🧩 Key Components

| Component | Purpose |
|-----------|---------|
| `PyPDFLoader` | Loads and parses PDF documents |
| `RecursiveCharacterTextSplitter` | Splits docs into 1000-char chunks (100-char overlap) |
| `HuggingFaceEmbeddings` | Converts chunks to dense vectors |
| `FAISS` | In-memory vector store for fast similarity search |
| `OllamaLLM (llama3)` | Generates the final grounded answer |

---

## 📝 Notes

- The vector store is held in memory — re-upload the PDF if the server restarts.
- For larger documents, consider persisting the FAISS index to disk with `db.save_local(...)`.
- Swap `llama3` for any other Ollama-compatible model (`mistral`, `phi3`, `qwen`, …) by changing the `model=` argument in `app.py`.

---

## 📜 License

MIT — see [LICENSE](../LICENSE).

