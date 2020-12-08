import pandas as pd
import string

def tokenize(sp_doc, allowed_pos_tags):
    def is_valid_token(t):
        return len(t.text) > 2 and t.is_alpha and not t.is_punct and not t.is_stop and t.pos_ in allowed_pos_tags

    return [t.lemma_.lower() for t in sp_doc if is_valid_token(t)]

def find_named_entities(sp_doc, allowed_entity_tags):
    entities = {}
    for ent in sp_doc.ents:
        if ent.label_ in allowed_entity_tags:
            entity_text = ent.text.replace("\s+", " ").strip(string.punctuation)
            if len(entity_text) > 2:
                if entity_text in entities:
                    entities[entity_text] += 1
                else:
                    entities[entity_text] = 1

    return entities

def find_emails_and_urls(sp_doc):
    results = []

    for tok in sp_doc:
        if tok.like_email or tok.like_url:
            results.append(tok.text.strip(string.punctuation).lower())

    return list(sorted(set(results)))

def output_named_entities_as_df(named_entities, num_values):
    data = [(k, v) for k, v in named_entities.items()]
    df = pd.DataFrame.from_records(data, columns=["Entity", "Frequency"])
    df = df.sort_values("Frequency", ascending=False)
    return df.head(num_values)
