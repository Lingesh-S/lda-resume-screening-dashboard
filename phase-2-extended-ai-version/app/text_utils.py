"""Text extraction and keyword-overlap scoring (no Streamlit or OpenAI imports)."""

import io
import os
import string

from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize


def extract_text(file) -> str:
    """Return the text of a .pdf, .docx or plain-text file.

    `file` may be a path or a file-like object with a `.name` (e.g. a
    Streamlit UploadedFile).
    """
    name = file if isinstance(file, (str, os.PathLike)) else getattr(file, "name", "")
    extension = os.path.splitext(str(name))[1].lower()

    if extension == ".pdf":
        import pdfplumber

        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if extension == ".docx":
        import docx

        return "\n".join(p.text for p in docx.Document(file).paragraphs)

    if isinstance(file, (str, os.PathLike)):
        with open(file, encoding="utf-8", errors="ignore") as handle:
            return handle.read()
    content = file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="ignore")
    if isinstance(file, io.IOBase):
        file.seek(0)
    return content


def process_text(text: str | None) -> list[str]:
    """Lower-case alphabetic tokens with English stopwords removed."""
    if not text:
        return []
    stop_words = set(stopwords.words("english"))
    return [w.lower() for w in word_tokenize(text) if w.isalpha() and w.lower() not in stop_words]


def calculate_score(job_description_tokens: list[str], resume_tokens: list[str]) -> float:
    """Percentage of job-description token occurrences that the resume covers (0-100)."""
    if not job_description_tokens:
        return 0.0
    frequency = FreqDist(job_description_tokens)
    covered = sum(frequency[token] for token in set(resume_tokens))
    return round(covered / len(job_description_tokens) * 100, 2)


def clean_for_prompt(resume_text: str) -> str:
    """Strip punctuation and stopwords to shorten the text sent to the LLM."""
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(resume_text.lower())
    return " ".join(t for t in tokens if t not in string.punctuation and t not in stop_words)
