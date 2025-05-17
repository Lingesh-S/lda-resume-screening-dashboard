# Phase 2 – AI-Powered Resume Screener (OpenAI Integration)

This version is an **extended upgrade** of the LDA-powered resume screener, using OpenAI’s API to intelligently generate interview questions based on resume content and job role.

## 🔍 What This Project Does

- Upload resume and job description
- Parse and analyze their content
- Uses OpenAI's GPT model to:
  - Understand resume–JD context
  - Generate tailored interview questions for the candidate

## 📁 Folder Structure

- `app/`: Contains the main Streamlit app (`app.py`)
- `data/`: Uploaded resumes and job descriptions (organized into folders)
- `Images/`: UI or branding images
- `ai_components/`: AI-related JSONs, prompt templates, future RAG logic
- `.env`: Stores your OpenAI API key (NOT uploaded to GitHub)

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

📌 Set up your .env file like this:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx

📦 Technologies Used
Python, Streamlit

OpenAI GPT API

Pandas, JSON

python-dotenv (for loading API key securely)

🧠 Future Upgrades
Resume scoring and ranking using embeddings

RAG-based document understanding

Recruiter chat assistant

Real-time feedback on resumes

👨‍💻 Author: Lingesh S
📍 Budding AI Engineer
🌐 GitHub • LinkedIn