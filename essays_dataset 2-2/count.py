import os
from nltk.tokenize import sent_tokenize, word_tokenize
from spellchecker import SpellChecker

# Read essay content from a file
def read_essay(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Count the number of sentences in a text
def count_sentences(text):
    essays_folder = 'essays'
    file_path = os.path.join(essays_folder, text)
    with open(file_path, 'r') as file:
        sent = file.read()
    sentences = sent_tokenize(sent)
    return len(sentences)

# Count misspelled words in a text
def count_misspelled_words(text):
    spell = SpellChecker()
    essays_folder = 'essays'
    file_path = os.path.join(essays_folder, text)
    with open(file_path, 'r') as file:
        word = file.read()
    words = word_tokenize(word)
    mispelled = spell.unknown(words)
    return len(mispelled)

