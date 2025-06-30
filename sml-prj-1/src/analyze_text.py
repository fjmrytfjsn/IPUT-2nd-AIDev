import spacy


def analyze_text(text):
    nlp = spacy.load("ja_ginza")
    doc = nlp(text)

    subject = ""
    predicate = ""

    for token in doc:
        if "subj" in token.dep_:
            subject = token.text
        if (
            "pred" in token.dep_
            or "ROOT" in token.dep_
            or "advcl" in token.dep_
            or "acl" in token.dep_
        ):
            predicate = token.text

    return subject, predicate
