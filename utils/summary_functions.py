import sys
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import string
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from heapq import nlargest
punctuations = string.punctuation
from spacy.language import Language
nlp = English()
nlp.add_pipe('sentencizer') # updated
parser = English()

filename = sys.argv[-1]
file = open(filename, 'rt')
text = file.read()
file.close()

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

def hello():
    print("wagwan g")

num_sentences_to_generate = 3
print("#############################")
print("SUMMARY")
print("#############################")
print(generate_summary(num_sentences_to_generate, text))
print("#############################")
print("ORIGINAL")
print("#############################")
print(text)