import pandas as pd
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")


def extract_named_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities


df = pd.read_csv('sentences_processed.csv')

df['Named Entities'] = df['Processed Sentences'].apply(extract_named_entities)


# Function to extract relationships using the specified pattern
def get_relation(sent):
    doc = nlp(sent)
    matcher = Matcher(nlp.vocab)

    # Define the pattern
    pattern = [{'DEP': 'ROOT'},
               {'DEP': 'prep', 'OP': "?"},  # Optional preposition
               {'DEP': 'agent', 'OP': "?"},  # Optional agent
               {'POS': 'ADJ', 'OP': "?"}]  # Optional adjective

    # Updated method to add pattern
    matcher.add("relationship_pattern", [pattern])  # No callback function is needed here

    matches = matcher(doc)
    relationships = []

    for match_id, start, end in matches:
        span = doc[start:end]
        relationships.append(span.text)

    return relationships


# Apply the function to your data
df['Relationships'] = df['Processed Sentences'].apply(get_relation)

# save to csv
df.to_csv('sentences_ner.csv', index=False)
