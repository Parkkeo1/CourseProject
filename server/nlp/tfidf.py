import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def identity_tokenizer(doc):
    return doc

def train_tfidf_vectorizer(sp_tokenized_docs, max_df=0.9, min_df=0.1):
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True,
                                       decode_error="ignore",
                                       tokenizer=identity_tokenizer,
                                       lowercase=False,
                                       max_df=0.8,
                                       min_df=0.1)
                                       # TODO move all constants to config

    fitted_tfidf_vectorizer = tfidf_vectorizer.fit(sp_tokenized_docs)
    return fitted_tfidf_vectorizer

def save_trained_tfidf_vocab(fitted_tfidf_vectorizer, picklename):
    with open(picklename, "wb") as f:
        pickle.dump(fitted_tfidf_vectorizer.vocabulary_, f)

def load_trained_tfidf_vocab(picklename):
    with open(picklename, "rb") as f:
        trained_tfidf_vocab = pickle.load(f)

    return trained_tfidf_vocab

def calculate_tfidf_for_new_doc(sp_tokenized_doc, trained_tfidf_vocab, max_df=0.9, min_df=0.1):
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True,
                                       decode_error="ignore",
                                       tokenizer=identity_tokenizer,
                                       lowercase=False,
                                       max_df=max_df,
                                       min_df=min_df,
                                       vocabulary=trained_tfidf_vocab)

    # TODO test with both transform() and fit_transform()
    tfidf_matrix = tfidf_vectorizer.fit_transform([sp_tokenized_doc])
    return tfidf_matrix, tfidf_vectorizer

def output_tfidf_for_new_doc_as_df(tfidf_matrix_row, tfidf_vectorizer, num_values=20):
    df = pd.DataFrame(tfidf_matrix_row.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False).round(3)
    return df.head(num_values)
