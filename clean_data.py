import re

import spacy
from spacy.matcher import Matcher

# read txt file
with open("pdfminer.txt", "r", encoding="utf-8") as f:
    text = f.read()

# download spacy model
# python -m spacy download en_core_web_md

nlp = spacy.load("en_core_web_md")
tokens = nlp(text)


from spacy.lang.en import English

nlp = English()
nlp.add_pipe("sentencizer")
doc = nlp(text)

print(list(doc.sents))
print(len(list(doc.sents)))



tokenized_text = [token.text for token in tokens]

# print(tokenized_text)

# remove stop words
stop_words = spacy.lang.en.stop_words.STOP_WORDS
tokenized_text = [token for token in tokenized_text if token not in stop_words]

# remove punctuation
punctuations = spacy.lang.punctuation.PUNCT
tokenized_text = [token for token in tokenized_text if token not in punctuations]

# print(tokenized_text)

# don't remove numbers

# remove whitespace
tokenized_text = [token for token in tokenized_text if token != " "]

# remove new line
tokenized_text = [token for token in tokenized_text if token != "\n"]

# remove empty string
tokenized_text = [token for token in tokenized_text if token != ""]

def preprocess_text(text):
    # Remove multiple newline characters and non-English letters
    cleaned_text = re.sub(r'[^A-Za-z0-9\n]+', ' ', text)
    # Keep numbers, replace multiple newlines with a single newline
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
    # Remove leading and trailing whitespace
    cleaned_text = cleaned_text.strip()
    return cleaned_text

# run each item through process_text
tokenized_text = [preprocess_text(token) for token in tokenized_text]

# reomve empty string
tokenized_text = [token for token in tokenized_text if token != ""]

# reomve single character strings
tokenized_text = [token for token in tokenized_text if len(token) > 1]

# remove number and whitespace only strings
def remove_number_whitespace_only(token):
    # "76", "76 6" reomve these
    if token.isdigit():
        return False
    # "76 6" reomve these
    if token.replace(" ", "").isdigit():
        return False
    return True

tokenized_text = [token for token in tokenized_text if remove_number_whitespace_only(token)]

# print(tokenized_text)
print(len(tokenized_text))

# Join the tokenized text into a single string
text = " ".join(tokenized_text)

# Process the text with spaCy
doc = nlp(text)

# save to text file
with open("cleaned_data.txt", "w", encoding="utf-8") as f:
    f.write(text)


# Iterate through the entities detected in the text
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")

matcher = Matcher(nlp.vocab)


