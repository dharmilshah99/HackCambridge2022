import spacy

def extract_keywords(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return doc.ents