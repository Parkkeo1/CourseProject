import os

class Config():
    SECRET_KEY = "placeholder"
    STATE_DIR = "data/"
    BASE_BIOS_FILENAME = STATE_DIR + "uiuc_base_bios.txt"
    BASE_URLS_FILENAME = STATE_DIR + "uiuc_base_urls.txt"
    CURR_URLS_FILENAME = STATE_DIR + "uiuc_curr_urls.txt"
    TRAINED_TFIDF_VOCAB_FILENAME = STATE_DIR + "tfidf.pkl"
