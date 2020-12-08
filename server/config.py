import os

class Config:
    SECRET_KEY = "placeholder"
    STATE_DIR = "data/"
    BIOS_FILENAME = STATE_DIR + "uiuc_bios.txt"
    URLS_FILENAME = STATE_DIR + "uiuc_urls.txt"
    TRAINED_TFIDF_FILENAME = STATE_DIR + "tfidf.pkl"
    TRAINED_LDA_FILENAME = STATE_DIR + "lda.pkl"

    KEY_CLASSES = set([
        "profile",
        "biography",
        "research",
        "education",
        "email",
        "phone",
        "title",
        "name",
        "content",
        "main",
    ])

    ALLOWED_POS_TAGS = set([
        "PROPN",
        "VERB",
        "NOUN",
        "ADJ"
    ])

    ALLOWED_ENT_TAGS = set([
        "PERSON",
        "ORG",
    ])

    TFIDF_PARAMS = {
        "max_df": 0.8,
        "min_df": 0.1,
        "num_values": 15
    }

    LDA_PARAMS = {
        "n_components": 20,
        "num_words_per_topic": 10,
        "num_topics": 5
    }

    NER_PARAMS = {
        "num_values": 10
    }
