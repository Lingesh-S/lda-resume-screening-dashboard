import io
from pathlib import Path

import pytest

text_utils = pytest.importorskip("text_utils")

JOBS_DIR = Path(__file__).resolve().parent.parent / "phase-2-extended-ai-version" / "data" / "JobDesc"


def nltk_ready():
    import nltk

    try:
        nltk.data.find("corpora/stopwords")
        nltk.data.find("tokenizers/punkt_tab")
        return True
    except LookupError:
        return False


needs_nltk = pytest.mark.skipif(not nltk_ready(), reason="NLTK stopwords/punkt_tab not downloaded")


def test_score_with_empty_job_description_is_zero():
    assert text_utils.calculate_score([], ["python"]) == 0.0


def test_score_counts_token_frequency():
    assert text_utils.calculate_score(["python", "python", "sql", "java"], ["python", "sql"]) == 75.0


@needs_nltk
def test_process_text_lowercases_and_drops_stopwords():
    assert text_utils.process_text("The Python and SQL!") == ["python", "sql"]
    assert text_utils.process_text(None) == []


def test_extract_text_from_uploaded_bytes():
    upload = io.BytesIO(b"plain resume text")
    upload.name = "resume.txt"
    assert text_utils.extract_text(upload) == "plain resume text"


def test_extract_text_from_bundled_job_description():
    path = JOBS_DIR / "Data Scientist.docx"
    assert "data" in text_utils.extract_text(str(path)).lower()
