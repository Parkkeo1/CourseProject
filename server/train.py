import spacy
from config import Config
from nlp.text_parser import *
from nlp.tfidf_lda import *

config = Config()

def train_new_tfidf_and_lda_from_base(nlp):
    with open(config.BIOS_FILENAME, encoding="utf8") as f:
        docs = list(nlp.pipe(f.readlines(), disable=["ner", "parser"]))

    print("Spacified all docs.", flush=True)

    tokenized_docs = [tokenize(d, config.ALLOWED_POS_TAGS) for d in docs]

    print("Tokenized all docs.", flush=True)

    tfidf_vectorizer = train_tfidf_vectorizer(tokenized_docs,
                                              config.TFIDF_PARAMS["max_df"],
                                              config.TFIDF_PARAMS["min_df"])

    print("Trained TF-IDF.", flush=True)

    tfidf_matrix = tfidf_vectorizer.transform(tokenized_docs)
    lda = train_lda(tfidf_matrix, config.LDA_PARAMS["n_components"])

    print("Trained LDA.", flush=True)

    save_trained_model(lda, config.TRAINED_LDA_FILENAME)
    save_trained_model(tfidf_vectorizer, config.TRAINED_TFIDF_FILENAME)

    print("Saved TF-IDF and LDA models.", flush=True)

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_lg")
    train_new_tfidf_and_lda_from_base(nlp)
