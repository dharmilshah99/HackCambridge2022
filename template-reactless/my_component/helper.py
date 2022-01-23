import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import string
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from heapq import nlargest
punctuations = string.punctuation
from spacy.language import Language
from wordcloud import WordCloud

def wordcloud_generator(audio_transcript):
    """Generate wordcloud image."""
    wordcloud_image = WordCloud(
        background_color="white"
    ).generate(audio_transcript)
    print(wordcloud_image)
    return wordcloud_image

nlp = English()
nlp.add_pipe('sentencizer')
parser = English()

def pre_process(document):
    clean_tokens = [ token.lemma_.lower().strip() for token in document ]
    clean_tokens = [ token for token in clean_tokens if token not in STOP_WORDS and token not in punctuations ]
    tokens = [token.text for token in document]
    lower_case_tokens = list(map(str.lower, tokens))
    
    return lower_case_tokens

def generate_numbers_vector(tokens):
    frequency = [tokens.count(token) for token in tokens]
    token_dict = dict(list(zip(tokens,frequency)))
    maximum_frequency=sorted(token_dict.values())[-1]
    normalised_dict = {token_key:token_dict[token_key]/maximum_frequency for token_key in token_dict.keys()}
    return normalised_dict

def sentences_importance(text, normalised_dict):
    importance ={}
    for sentence in nlp(text).sents:
        for token in sentence:
            target_token = token.text.lower()
            if target_token in normalised_dict.keys():
                if sentence in importance.keys():
                    importance[sentence]+=normalised_dict[target_token]
                else:
                    importance[sentence]=normalised_dict[target_token]
    return importance

def generate_summary(rank, text):
    target_document = parser(text)
    importance = sentences_importance(text, generate_numbers_vector(pre_process(target_document)))
    summary = nlargest(rank, importance, key=importance.get)
    return summary

def extract_keywords(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return doc.ents