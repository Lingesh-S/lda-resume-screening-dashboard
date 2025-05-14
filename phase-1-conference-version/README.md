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
streamlit run streamlit_app.py
```
## Files

- streamlit_app.py: Main Streamlit app.
- Resume_Data.csv: Preprocessed resumes.
- Job_Data.csv: Job descriptions.
- Similar.py: Custom similarity scoring module.
- Images/logo.png: Logo displayed in the app.

## Dependencies
- Streamlit
- Gensim
- pandas
- plotly
- matplotlib
- WordCloud
- nltk
- PIL