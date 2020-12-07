import spacy
from nlp.config import Config
from nlp.tokenizer import spacify_doc, tokenize
from nlp.tfidf import train_tfidf_vectorizer, save_trained_tfidf_vocab

config = Config()

def train_new_tfidf_from_base(nlp):
    with open(config.BASE_BIOS_FILENAME, encoding="utf8") as f:
        docs = [spacify_doc(b.replace("\s+", " ").strip(), nlp) for b in f.readlines()]

    print("Spacified all docs.")

    tokenized_docs = [tokenize(d) for d in docs]

    print("Tokenized all docs.")

    fitted_tfidf_vectorizer = train_tfidf_vectorizer(tokenized_docs)
    save_trained_tfidf_vocab(fitted_tfidf_vectorizer, config.TRAINED_TFIDF_VOCAB_FILENAME)

    print("Trained and saved TF-IDF vocabulary.")

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_md")
    train_new_tfidf_from_base(nlp)
