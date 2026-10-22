# Phase 1 – Resume Screening App

This version was presented at the ICCCAI 2024 conference. It includes:

- Resume parsing and topic modeling using LDA
- Resume–Job description matching
- Streamlit-based interactive dashboard
- Token visualization


📍 Presented at: ICCCAI 2024  
🏛 Hosted by: Taylor’s University, Malaysia  
📄 Paper Published in Conference Proceedings


This Streamlit application performs automatic resume screening using TF-IDF and LDA topic modeling.

## 🔍 Project Description

A Streamlit-based application that performs resume screening using LDA topic modeling, token indexing, and semantic similarity. It helps recruiters identify top-matching candidates based on uploaded resumes and job descriptions.

## 📂 Folder Structure

- `app/`: Main Streamlit app
- `core/`: Utility scripts like cleaner, TF-IDF, and similarity functions
- `data/`: Input datasets (resume & job descriptions)
- `Images/`: App branding/logo
- `notebooks/`: Jupyter exploration notebook
- `installers/`: Batch scripts to install dependencies

## Features
- Load and parse resumes and job descriptions from CSV.
- Match resumes with job descriptions using a custom similarity module.
- Rank resumes based on matching score.
- Visualize LDA topics using word clouds and bar charts.

## How to Run

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt punkt_tab stopwords wordnet
streamlit run app/app.py
```

The app finds its data and logo relative to its own file, so it can be started from any folder.

## Files

- `app/app.py`: Streamlit dashboard. Scores are cached per job description and the LDA model is trained once per dataset.
- `core/fileReader.py`: builds `data/Resume_Data.csv` / `data/Job_Data.csv` from a folder of .pdf/.docx/.txt files or from the Kaggle CSV.
- `core/Cleaner.py`, `core/Distill.py`: tokenising, stopword removal, lemmatisation (spaCy + NLTK).
- `core/tf_idf.py`: selects distinctive words for matching.
- `core/Similar.py`: word-level Jaccard, Sørensen–Dice, cosine and overlap similarity, averaged to a 0–100 score.
- `data/Resume_Data.csv`: anonymised sample of the public Kaggle resume dataset (`data/resume_dataset.csv`).
- `data/Job_Data.csv`: processed job descriptions.

## Note on scores

Earlier versions compared resumes and job descriptions character by character (textdistance's default
on plain strings), which made almost every pair look similar. Scores now compare words, so they spread
out more and rankings are more meaningful.
