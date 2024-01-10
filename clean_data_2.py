import re
import spacy
import pandas as pd

# Read the text file
with open("pdfminer.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Load the spaCy model and split the text into sentences
nlp = spacy.load("en_core_web_md")
doc = nlp(text)
sentences = list(doc.sents)

# Create a dataframe to store the sentences
df = pd.DataFrame({'Sentences': sentences})

# save the dataframe as a csv file
df.to_csv('sentences.csv', index=False)

# read
df = pd.read_csv('sentences.csv')


def preprocess_text(text):
    # Remove multiple newline characters and non-English letters
    cleaned_text = re.sub(r'[^A-Za-z0-9\n]+', ' ', text)
    # Keep numbers, replace multiple newlines with a single newline
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
    # Remove leading and trailing whitespace
    cleaned_text = cleaned_text.strip()
    return cleaned_text


df['Processed Sentences'] = df['Sentences'].apply(preprocess_text)

df = df[df['Processed Sentences'].str.len() > 1]

# save
df.to_csv('sentences_processed.csv', index=False)

