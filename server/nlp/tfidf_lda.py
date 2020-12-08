import pandas as pd
import pickle
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer

def identity_tokenizer(doc):
    return doc

def save_trained_model(trained_model, picklename):
    with open(picklename, "wb") as f:
        pickle.dump(trained_model, f)

def load_trained_model(picklename):
    with open(picklename, "rb") as f:
        trained_model = pickle.load(f)

    return trained_model

def train_tfidf_vectorizer(sp_tokenized_docs, max_df, min_df):
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True,
                                       decode_error="ignore",
                                       tokenizer=identity_tokenizer,
                                       lowercase=False,
                                       max_df=max_df,
                                       min_df=min_df)
    tfidf_vectorizer.fit(sp_tokenized_docs)
    return tfidf_vectorizer

def train_lda(tfidf_matrix, n_components):
    lda = LatentDirichletAllocation(n_components=n_components, learning_method='online')
    lda.fit(tfidf_matrix)
    return lda

def calculate_tfidf_for_new_doc(sp_tokenized_doc, trained_tfidf_vectorizer):
    tfidf_matrix = trained_tfidf_vectorizer.transform([sp_tokenized_doc])
    return tfidf_matrix

def calculate_lda_for_new_doc(tfidf_matrix, trained_lda):
    lda_topic_dist = trained_lda.transform(tfidf_matrix)
    return lda_topic_dist

def output_tfidf_for_new_doc_as_df(tfidf_matrix_row, tfidf_vectorizer, num_values):
    df = pd.DataFrame(tfidf_matrix_row.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["TF-IDF"])
    df = df.reset_index().rename(columns = {"index": "Term"}).sort_values('TF-IDF', ascending=False).round(3)
    return df.head(num_values)

def output_lda_for_new_doc_as_df(lda_topic_dist, trained_lda, feature_names, num_words_per_topic, num_topics):
    comps = trained_lda.components_
    topic_words = [ ", ".join([ feature_names[i] for i in topic.argsort()[:-num_words_per_topic - 1:-1]]) for topic in comps ]
    topic_words_and_dist = list(zip(topic_words, lda_topic_dist))
    df = pd.DataFrame.from_records(topic_words_and_dist, columns=["Topic Words", "Coverage"])
    df = df.sort_values("Coverage", ascending=False).round(3)
    return df.head(num_topics)
