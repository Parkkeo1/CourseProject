import spacy
from nlp.config import state_dir, base_bios_filename, base_urls_filename, curr_urls_filename
from nlp.tokenizer import spacify_doc, tokenize
from nlp.tfidf import train_tfidf_vectorizer, save_trained_tfidf_vocab

def train_new_tfidf_from_base(nlp):
    with open(base_bios_filename, encoding="utf8") as f:
        docs = [spacify_doc(b.replace("\s+", " ").strip(), nlp) for b in f.readlines()]

    print("Spacified all docs.")

    tokenized_docs = [tokenize(d) for d in docs]

    print("Tokenized all docs.")

    fitted_tfidf_vectorizer = train_tfidf_vectorizer(tokenized_docs)
    save_trained_tfidf_vocab(fitted_tfidf_vectorizer, state_dir + "tfidf.pkl")

    print("Trained and saved TF-IDF vocabulary.")

    with open(base_urls_filename, encoding="utf8") as f:
        curr_urls = [u.replace("\s+", " ").strip() for u in f.readlines()]

    # track urls currently used in training vocab
    with open(curr_urls_filename, "w", encoding="utf8") as f:
        for u in curr_urls:
            f.write(u)
            f.write("\n")

    print("Updated the list of currently used URLs in the TF-IDF vocabulary.")

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_md")
    train_new_tfidf_from_base(nlp)
