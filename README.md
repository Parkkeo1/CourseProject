# Keon Park - CS 410 CourseProject
**Extracting relevant information from faculty bios (2.2)**

This repository contains the source code, data, and documentation for Keon (Isaac) Park's final project for CS 410 Fall 2020 at UIUC. This project is an extension/spin-off of the *ExpertSearch* system that seeks to build upon ExpertSearch's NLP features by extracting not only names and emails from faculty pages but also keywords, named entities, and topics  in order to provide users with a more comprehensive overview without having to manually visit the page.

This project was an individual effort by Keon (Isaac) Park.

### Software Usage Tutorial Presentation

The link to the tutorial video for this project is [here](). The video is a brief explanation of how to locally install/run and use the project code, including a example use case. The rest of this README document also provides details regarding this software's functionality and implementation.

### Overview

### Implementation

### Local Setup

These instructions assume the user is already knowledgeable of git and Python environments and has Python 3 (note: 3.7 was used during development) with pip installed.

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
