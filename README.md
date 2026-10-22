# 📄 LDA-Powered Resume Screening Dashboard

A dual-phase intelligent resume screening system combining NLP, topic modeling, and interactive UI for recruiters.  
🚀 Extended in Phase 2 with OpenAI-powered interview question generation!

---

## ⚙ Technologies Used

- Python 🐍  
- NLP with SpaCy & Gensim  
- LDA Topic Modeling  
- Streamlit for Dashboard UI  
- Pandas & NumPy for data processing  
- Matplotlib & pyLDAvis for visualization  
- OpenAI API (Phase 2)

---

## 🚀 Key Features

### 🧪 Phase 1: Conference Version
- 📄 Upload and parse resumes (PDF)
- 🧠 Extract dominant topics using LDA
- 🧩 Match resume topics with job descriptions
- 📊 Interactive visualization of token weights and match scores
- 📂 Paper-focused, academic-grade prototype

### 🤖 Phase 2: Extended AI Version
- 🔍 AI-based screening & candidate ranking
- 🗣️ Auto-generated interview questions based on job role + resume
- 🔌 OpenAI GPT-3.5 integration
- ⚠️ Includes a working version and a "buggy" prototype folder

---

## 📘 Conference Info

- 📍 **ICCCAI 2024** – International Conference on Cognitive Computing and Artificial Intelligence  
- 🏛 In association with **Taylor’s University, Malaysia**
- 📅 Held on **March 7–8, 2024**
- 📄 **Paper published** in internal proceedings
- 👨‍🎓 Represented by: **Lingesh S (Author)**

---

## 📈 Future Work

- 🔌 Integration with OpenAI embeddings for smarter screening
- 🧠 RAG-based document understanding (Retrieval Augmented Generation)
- 💡 Resume-score-based recommendation engine
- 🌐 Web deployment with modern AI microservices

---

## 🗂 Repository Structure

```text
lda-resume-screening-dashboard/
├── phase-1-conference-version/     # ICCCAI 2024 version: LDA topics + similarity ranking
│   ├── app/app.py                  # Streamlit dashboard
│   ├── core/                       # Cleaning, TF-IDF, similarity, dataset builder
│   ├── data/                       # Processed resumes (anonymised Kaggle sample) + job descriptions
│   └── notebooks/                  # Exploration notebook
├── phase-2-extended-ai-version/    # Adds accounts, resume upload and OpenAI interview questions
│   ├── app/                        # app.py (UI), auth.py (hashed accounts), text_utils.py
│   ├── data/JobDesc/               # Job descriptions offered in the app
│   └── .env.example                # OPENAI_API_KEY, OPENAI_MODEL
├── tests/                          # pytest suite for both phases (unit + Streamlit smoke tests)
├── requirements.txt                # Both phases
└── requirements-dev.txt            # + pytest, ruff
```

---

## 🚀 Quick start

Requires Python 3.10+.

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt punkt_tab stopwords wordnet

# Phase 1 dashboard
streamlit run phase-1-conference-version/app/app.py

# Phase 2 (needs an OpenAI key)
cp phase-2-extended-ai-version/.env.example phase-2-extended-ai-version/.env   # then add your key
streamlit run phase-2-extended-ai-version/app/app.py
```

**Use your own resumes in phase 1:** put .pdf/.docx/.txt files in a folder and rebuild the dataset:

```bash
cd phase-1-conference-version
python core/fileReader.py folder --input /path/to/resumes --output data/Resume_Data.csv
```

The bundled `Resume_Data.csv` is an anonymised sample (2 resumes per category) of the public
[Kaggle resume dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset), rebuilt with
`python core/fileReader.py kaggle --input data/resume_dataset.csv --output data/Resume_Data.csv`.

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
ruff check .
pytest            # about 30 seconds; includes headless runs of both apps
```

## 🔒 Privacy

Real people's resumes and user accounts are never committed: `.gitignore` excludes `data/Resumes/`
and `ai_components/users.json`. Phase 2 stores passwords as salted PBKDF2 hashes, but it is a local
demo, not production authentication.

---

## 👨‍💻 Author

**Lingesh S**  
📍 Budding AI Engineer passionate about smart solutions and real-world applications.  
🌐 [GitHub](https://github.com/Lingesh-S) • [LinkedIn](https://linkedin.com/in/lingesh-s29) • [X](https://x.com/LINGESH_S29)

---

> 💡 *For any questions or collaboration ideas, feel free to connect on LinkedIn!*
