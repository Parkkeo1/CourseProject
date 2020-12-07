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
from nlp.html_parser import get_relevant_html_tags, extract_text_from_tags
from nlp.tokenizer import spacify_doc, tokenize
from nlp.tfidf import load_trained_tfidf_vocab, calculate_tfidf_for_new_doc,  output_tfidf_for_new_doc_as_df

class URLForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit")

driver_ = None
nlp_ = None
tfidf_vocab_ = None
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
        nlp_ = spacy.load("en_core_web_md")
    return nlp_

def get_tfidf_vocab():
    global tfidf_vocab_
    if tfidf_vocab_ is None:
        tfidf_vocab_ = load_trained_tfidf_vocab(app.config["TRAINED_TFIDF_VOCAB_FILENAME"])
    return tfidf_vocab_

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

    # return "\n".join([str(r) for r in relevant_tags])

    # get text from all relevant tags
    text = extract_text_from_tags(relevant_tags)
    nlp = get_spacy_nlp()
    sp_doc = spacify_doc(text, nlp)

    # TODO get named NER from relevant tags

    # Get TF-IDF weights from saved/trained model/vocab
    sp_tokens = tokenize(sp_doc)
    vocab = get_tfidf_vocab()

    tfidf_matrix, tfidf_vectorizer = calculate_tfidf_for_new_doc(sp_tokens, vocab)
    tfidf_df = output_tfidf_for_new_doc_as_df(tfidf_matrix[0], tfidf_vectorizer, 10)

    # TODO fill in template html with results data (TF-IDF, NER, even LDA?)
    return render_template("results.html", query_url=query_url, tfidf=tfidf_df.to_html())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
