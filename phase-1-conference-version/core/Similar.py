"""Similarity scoring between a resume and a job description."""

import textdistance as td


def _tokens(text):
    """Split a whitespace-joined token string into a list of words.

    textdistance compares characters when given plain strings, which makes
    almost every pair of documents look similar. Comparing word lists keeps
    the score meaningful. Non-string values (such as pandas NaN) count as empty.
    """
    if isinstance(text, str):
        return text.split()
    if isinstance(text, (list, tuple, set)):
        return list(text)
    return []


def match(resume, job_des):
    """Return a 0-100 match score averaged over four token-set similarity metrics."""
    resume_tokens = _tokens(resume)
    job_tokens = _tokens(job_des)
    if not resume_tokens or not job_tokens:
        return 0.0

    scores = (
        td.jaccard.similarity(resume_tokens, job_tokens),
        td.sorensen_dice.similarity(resume_tokens, job_tokens),
        td.cosine.similarity(resume_tokens, job_tokens),
        td.overlap.normalized_similarity(resume_tokens, job_tokens),
    )
    return sum(scores) / len(scores) * 100
