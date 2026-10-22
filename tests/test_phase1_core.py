import math

import pytest

import Similar
import tf_idf


def test_identical_documents_score_100():
    assert Similar.match("python sql pandas", "python sql pandas") == pytest.approx(100)


def test_disjoint_documents_score_0():
    assert Similar.match("python sql", "teaching english") == 0


def test_partial_overlap_is_between():
    score = Similar.match("python sql pandas", "python java")
    assert 0 < score < 100


def test_scores_compare_words_not_characters():
    # Same letters, different words: character-level comparison would call this ~100.
    assert Similar.match("listen", "silent") == 0


@pytest.mark.parametrize("missing", [None, float("nan"), ""])
def test_missing_text_scores_0(missing):
    assert Similar.match(missing, "python") == 0
    assert Similar.match("python", missing) == 0


def test_tfidf_handles_empty_and_short_input():
    assert tf_idf.do_tfidf([]) == ""
    assert tf_idf.do_tfidf([""]) == ""


def test_tfidf_returns_words_from_input():
    tokens = [f"word{i}" for i in range(200)] + ["common"] * 100
    words = tf_idf.do_tfidf(tokens).split()
    assert words and "common" not in words
    assert not any(isinstance(w, float) and math.isnan(w) for w in words)


def test_remove_stopwords_does_not_mutate_shared_list():
    Distill = pytest.importorskip("Distill", reason="needs spaCy en_core_web_sm and NLTK stopwords")
    before = list(Distill.stop_words)
    result = Distill.remove_stopwords(["the", "python", "extra"], optional_params=True, optional_words=["extra"])
    assert result == ["python"]
    assert Distill.stop_words == before
