import re

import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Define english stopwords
stop_words = stopwords.words('english')

# load the spacy module and create a nlp object
# This need the spacy en module to be present on the system.
nlp = spacy.load('en_core_web_sm')
# proces to remove stopwords form a file, takes an optional_word list
# for the words that are not present in the stop words but the user wants them deleted.


def remove_stopwords(text, stopwords=None, optional_params=False, optional_words=None):
    """Drop stopwords (plus any `optional_words`) without mutating the shared list."""
    stop = set(stop_words if stopwords is None else stopwords)
    if optional_params and optional_words:
        stop.update(optional_words)
    return [word for word in text if word not in stop]


def tokenize(text):
    # Removes any useless punctuations from the text
    text = re.sub(r'[^\w\s]', '', text)
    return word_tokenize(text)


def lemmatize(text):
    # the input to this function is a list
    str_text = nlp(" ".join(text))
    lemmatized_text = []
    for word in str_text:
        lemmatized_text.append(word.lemma_)
    return lemmatized_text

# internal fuction, useless right now.


def _to_string(List):
    # the input parameter must be a list
    string = " "
    return string.join(List)


def remove_tags(text, postags=('PROPN', 'NOUN', 'ADJ', 'VERB', 'ADV')):
    """
    Takes in Tags which are allowed by the user and then elimnates the rest of the words
    based on their Part of Speech (POS) Tags.
    """
    filtered = []
    str_text = nlp(" ".join(text))
    for token in str_text:
        if token.pos_ in postags:
            filtered.append(token.text)
    return filtered
