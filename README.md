# Keon Park - CS 410 CourseProject
**Extracting relevant information from faculty bios (2.2)**

This repository contains the source code, data, and documentation for Keon (Isaac) Park's final project for CS 410 Fall 2020 at UIUC. This project is an extension/spin-off of the *ExpertSearch* system that seeks to build upon ExpertSearch's NLP features by extracting not only names and emails from faculty pages but also keywords, named entities, and topics  in order to provide users with a more comprehensive overview without having to manually visit the page.

This project was an individual effort by Keon (Isaac) Park.

### Software Usage Tutorial Presentation

The link to the tutorial video for this project is [here](). The video is a brief explanation of how to locally install/run and use the project code, including a example use case. The rest of this README document also provides details regarding this software's functionality and implementation.

### Overview

As previously mentioned, this project is a standalone extension of the *ExpertSearch* system that provides improved NLP features to better analyze text in faculty web pages. In its current implementation, *ExpertSearch* only extracts the name and email of the faculty member from the page, limiting its use as a tool for users seeking more in-depth overviews of faculty members and their biographies. As a result, this project was developed with more advanced text retrieval and mining features to automatically provide users with a useful "snapshot" of faculty page content.

It accomplishes this by scraping, processing, and analyzing text data from faculty pages via URLs entered by the user using `BeautifulSoup`, `spaCy`, `scikit-learn`, and pre-trained TF-IDF and LDA models (available as `.pkl` files in the `server/data` directory) to automatically extract/calculate relevant keywords, named entities, and topics. For example, here is a screenshot of the system's results for UIUC Professor [Tarek Abdelzaher](https://cs.illinois.edu/about/people/all-faculty/zaher):

![Screenshot](https://raw.githubusercontent.com/Parkkeo1/CourseProject/main/project_example_image.PNG)

As shown above, this software, like *ExpertSearch* includes the likely name and emails of the faculty member. It also provides detailed overviews of the system's calculated keywords, named entities, and topics with specific numbers to provide users with an effective "snapshot" of the page without visting it manually. For example, the user can deduce that Professor Abdelzaher is likely to be an engineering (likely CS or CompE, due to keywords like `system`, `transactions`, and `data`) research professor involved/related with the Institute of Electrical and Electronics Engineers (IEEE).

### Implementation

This project/system is implemented as a Flask web application with a Python backend and HTML/CSS frontend. The code is organized like a standard Flask application, in the following directory structure (not all files shown):

```
CourseProject/
│   README.md
│   .gitignore
|   ...
└───server/
    │   app.py
    │   train.py
    │   config.py
    │   requirements.txt
    └───data/
        │   tfidf.pkl
        |   uiuc_bios.txt
        |   ...
    └───nlp/
        │   scraper.py
        |   html_parser.py
        |   tfidf_lda.py
        |   ...
    └───static/
        │   main.css
    └───templates/
        │   base.html
        |   ...
```

TODO


### Local Setup

These instructions assume the user is already knowledgeable of `git` and `Python` environments and has `Python 3` (note: 3.7 was used during development) with `pip` installed.

1. Clone this repository

```bash
git clone https://github.com/Parkkeo1/CourseProject.git
cd CourseProject
```

2. Create a new Python venv and install dependencies

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r server/requirements.txt
```

3. Launch the software.

```bash
cd server
python train.py           // if you want to to newly train and save a TF-IDF and LDA model based on the data in data/uiuc_bios.txt to be later used by the Flask app.
python app.py             // if you want to launch the project's main application, the Flask app.
```

If you launched the Flask app, navigate to `localhost:5000` in your web browser to view and use the Flask app.
