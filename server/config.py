import os

class Config:
    SECRET_KEY = "placeholder"
    STATE_DIR = "data/"
    BIOS_FILENAME = STATE_DIR + "uiuc_base_bios.txt"
    URLS_FILENAME = STATE_DIR + "uiuc_base_urls.txt"
    TRAINED_TFIDF_VOCAB_FILENAME = STATE_DIR + "tfidf.pkl"
    KEY_CLASSES = set([
        "profile",
        "biography",
        "research",
        "education",
        "email",
        "phone",
        "title",
        "name"
    ])
