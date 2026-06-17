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
