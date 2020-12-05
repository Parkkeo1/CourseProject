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
from nlp.tokenizer import spacify_doc

class URLForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit")

driver_ = None
nlp_ = None
app = Flask(__name__)
app.config.from_object(Config)

key_classes = set([
    "profile",
    "biography",
    "research",
    "education",
    "email",
    "phone",
    "title",
    "name"
])

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

@app.route("/", methods=["GET", "POST"])
def home():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for("query", query_url=form.url.data))

    return render_template("home.html", form=form)

@app.route("/query/<query_url>")
def query(query_url):
    if not query_url:
        return "Invalid Query"

    return query_url

    # nlp = get_spacy_nlp()
    # driver = get_webdriver()

    # soup = scrape_url(query_url, driver)
    # relevant_tags = get_relevant_html_tags(soup, key_classes)
    #
    # # TODO get named NER from matching + relevant tag classes
    #
    # # get text from all relevant tags
    # text = extract_text_from_tags(relevant_tags)
    # sp_doc = spacify_doc(text, nlp)
    # sp_tokens = tokenize(sp_doc)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
