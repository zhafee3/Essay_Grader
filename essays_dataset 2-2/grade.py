import os
import spacy
import numpy as np
from scipy.spatial.distance import cosine
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from count import read_essay, count_sentences, count_misspelled_words
from score import score_spelling, score_length

nlp = spacy.load('en_core_web_md')

def parse_essay(essay_text):
    return nlp(essay_text)

def sentence_embedding(sentence):
    doc = nlp(sentence)
    vectors = [token.vector for token in doc if token.has_vector and not token.is_stop]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros((nlp.vocab.vectors_length,))

def check_sentence_structure(sentence):
    errors = {
        "missing_main_verb": not any(tok.pos_ == "VERB" for tok in sentence),
        "incorrect_start": sentence[0].pos_ not in ["NOUN", "PROPN", "ADV", "ADP", "SCONJ", "AUX", "PRON", "INTJ"],
        "missing_subject": not any(tok.dep_ == "nsubj" or tok.dep_ == "nsubjpass" for tok in sentence),
        "missing_determiners": any(token.pos_ == 'NOUN' and not any(child.dep_ == 'det' for child in token.children) for token in sentence),
        "subordinate_clause_error": any(token.dep_ == 'mark' and not any(child.dep_ in ['csubj', 'ccomp'] for child in token.head.children) for token in sentence)
    }
    return errors

def evaluate_sentences(doc):
    results = []
    for sent in doc.sents:
        sentence_errors = check_sentence_structure(sent)
        results.append(sentence_errors)
    return results

def essay_coherence(sentences):
    embeddings = [sentence_embedding(sent) for sent in sentences]
    if len(embeddings) > 1:
        similarities = [1 - cosine(embeddings[i], embeddings[i+1]) for i in range(len(embeddings)-1)]
        return np.mean(similarities), np.std(similarities)
    else:
        return 0, 0

def extract_topic(prompt):
    parts = prompt.split('.')  # Assuming parts are separated by periods
    if len(parts) > 1:
        return parts[1].strip()  # Return the second part, strip any leading/trailing whitespace
    return ""

def topic_relevance(essay_text, prompt):
    topical_part = extract_topic(prompt)
    prompt_embedding = sentence_embedding(topical_part)

    essay_sentences = sent_tokenize(essay_text)
    essay_embeddings = [sentence_embedding(sentence) for sentence in essay_sentences]
    if essay_embeddings:
        average_essay_embedding = np.mean(essay_embeddings, axis=0)
        score= 1 - cosine(average_essay_embedding, prompt_embedding)
        return score
    return 0

def relevance_Score(score):

    if score > 0.63:
        return 5
    if score > 0.6:
        return 4
    if score > 0.59:
        return 3
    if score > 0.53:
        return 2
    if score > 0.1:
        return 1




#original grammar_error
def identify_grammar_errors(tagged_words):
    agreement_errors = 0
    verb_tense_errors = 0
    for i in range(len(tagged_words) - 1):
        current_word, current_tag = tagged_words[i]
        next_word, next_tag = tagged_words[i + 1]
        if current_tag in ['NN', 'NNP'] and next_tag == 'VBP':
            agreement_errors += 1
        elif current_tag == 'NNS' and next_tag == 'VBZ':
            agreement_errors += 1
        if current_tag == 'MD' and next_tag not in ['VB']:
            verb_tense_errors += 1
    return agreement_errors, verb_tense_errors


def grammar_score(agreement_errors, verb_tense_errors):
    errors = agreement_errors + verb_tense_errors
    if errors > 5:
        return 1
    elif errors > 3:
        return 2
    elif errors > 1:
        return 3
    elif errors > 0:
        return 4
    else:
        return 5


def pTag(text):
    essays_folder = 'essays'
    file_path = os.path.join(essays_folder, text)
    with open(file_path, 'r') as file:
        content = file.read()
    words = word_tokenize(content)
    tagged = pos_tag(words)
    return tagged
