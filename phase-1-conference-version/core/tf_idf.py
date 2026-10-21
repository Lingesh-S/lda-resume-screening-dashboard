"""TF-IDF keyword selection used to build the `TF_Based` column."""

from sklearn.feature_extraction.text import TfidfVectorizer


def do_tfidf(token):
    """Return the distinctive words in a list of tokens as one space-joined string.

    Each token is treated as a document, so `max_df` drops words that repeat
    across the text and keeps the rarer, more specific ones. Returns an empty
    string when nothing survives the pruning (very short documents).
    """
    tokens = [t for t in token if t and t.strip()]
    if not tokens:
        return ""
    tfidf = TfidfVectorizer(max_df=0.05, min_df=0.002)
    try:
        tfidf.fit_transform(tokens)
    except ValueError:
        # "After pruning, no terms remain" or "empty vocabulary"
        return ""
    return " ".join(tfidf.get_feature_names_out())
