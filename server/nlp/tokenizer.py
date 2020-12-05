def spacify_doc(doc, nlp):
    return nlp(doc)

def tokenize(sp_doc):
    def is_valid_token(t):
        return len(t.text) > 1 and t.is_alpha and not t.is_punct and not t.is_stop

    return [t.lemma_.lower() for t in sp_doc if is_valid_token(t)]

# TODO NER with spacy "PERSON" entities
