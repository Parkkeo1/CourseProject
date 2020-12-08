from flask import Flask, redirect, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import spacy

from config import Config
from nlp.scraper import scrape_url
from nlp.html_parser import *
from nlp.text_parser import *
from nlp.tfidf_lda import *

class URLForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit")

driver_ = None
nlp_ = None
tfidf_ = None
lda_ = None
app = Flask(__name__)
app.config.from_object(Config)

def get_webdriver():
    global driver_
    if driver_ is None:
        options = Options()
        options.headless = True
        driver_ = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver_

def get_spacy_nlp():
    global nlp_
    if nlp_ is None:
        nlp_ = spacy.load("en_core_web_lg")
    return nlp_

def get_tfidf():
    global tfidf_
    if tfidf_ is None:
        tfidf_ = load_trained_model(app.config["TRAINED_TFIDF_FILENAME"])
    return tfidf_

def get_lda():
    global lda_
    if lda_ is None:
        lda_ = load_trained_model(app.config["TRAINED_LDA_FILENAME"])
    return lda_

@app.route("/", methods=["GET", "POST"])
def home():
    form = URLForm()
    if form.validate_on_submit():
        redirect_url = "/query?q={}".format(form.url.data)
        return redirect(redirect_url)

    return render_template("home.html", form=form)

@app.route("/query")
def query():
    query_url = request.args.get("q", default="", type=str)

    if not query_url:
        return "Invalid Query" # TODO display results.html template with "Invalid Query" message.

    driver = get_webdriver()
    soup = scrape_url(query_url, driver)
    relevant_tags = get_relevant_html_tags(app.config["KEY_CLASSES"], soup)

    # get text from all relevant tags
    text = extract_text_from_tags(relevant_tags)

    nlp = get_spacy_nlp()
    sp_doc = nlp(text)

    # get named entities and possible emails/urls from relevant tags
    named_entities = find_named_entities(sp_doc, app.config["ALLOWED_ENT_TAGS"])
    emails_and_urls = find_emails_and_urls(sp_doc)

    # Get TF-IDF weights from saved vectorizer on new doc text
    sp_tokens = tokenize(sp_doc, app.config["ALLOWED_POS_TAGS"])
    tfidf_vectorizer = get_tfidf()
    tfidf_matrix = calculate_tfidf_for_new_doc(sp_tokens, tfidf_vectorizer)

    # Get LDA topic distribution for doc
    lda_model = get_lda()
    lda_topics = calculate_lda_for_new_doc(tfidf_matrix, lda_model)

    tfidf_params = app.config["TFIDF_PARAMS"]
    lda_params = app.config["LDA_PARAMS"]
    ner_params = app.config["NER_PARAMS"]

    # generate dataframes for easy output as html
    tfidf_df = output_tfidf_for_new_doc_as_df(tfidf_matrix[0],
                                              tfidf_vectorizer,
                                              tfidf_params["num_values"])

    lda_df = output_lda_for_new_doc_as_df(lda_topics[0],
                                          lda_model,
                                          tfidf_vectorizer.get_feature_names(),
                                          lda_params["num_words_per_topic"],
                                          lda_params["num_topics"])

    entities_df = output_named_entities_as_df(named_entities, ner_params["num_values"])

    likely_faculty_name = str(entities_df["Entity"].iloc[entities_df["Frequency"].argmax()])

    # TODO fill in template html with results data (TF-IDF, NER, LDA)
    return render_template("results.html",
                           query_url=query_url,
                           tfidf=tfidf_df.to_html(index=False),
                           entities=entities_df.to_html(index=False),
                           lda=lda_df.to_html(index=False),
                           emails_and_urls=", ".join(emails_and_urls),
                           likely_faculty_name=likely_faculty_name,
                           tfidf_num_values=tfidf_params["num_values"],
                           lda_num_topics=lda_params["num_topics"],
                           ner_num_values=ner_params["num_values"])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
