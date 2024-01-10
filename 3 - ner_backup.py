import pandas as pd
import spacy
from spacy.matcher import Matcher
from tqdm import tqdm

nlp = spacy.load("en_core_web_md")


def extract_named_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities


df = pd.read_csv('sentences_processed.csv')

df['Named Entities'] = df['Processed Sentences'].apply(extract_named_entities)

# Initialize the Matcher
matcher = Matcher(nlp.vocab)


# # Define your patterns
# patterns = [
#     {"label": "ORG", "pattern": [{"lower": "apple"}]},
#     {"label": "PRODUCT", "pattern": [{"lower": "iphone"}, {"is_digit": True}]}
# ]
#
# # Add your patterns to the Matcher
# for pattern in patterns:
#     matcher.add(pattern["label"], [pattern["pattern"]])
#


# patterns = [
#     [{"DEP": "ROOT"}],
#     [{"DEP": "prep", "OP": "?"}],
#     [{"DEP": "agent", "OP": "?"}],
#     [{"POS": "ADJ", "OP": "?"}]
# ]
#
# # Initialize the Matcher
# matcher = Matcher(nlp.vocab)
#
# # Add your patterns to the Matcher
# for pattern in patterns:
#     matcher.add("CUSTOM_PATTERN", [pattern])

# def extract_relationships(text):
#     doc = nlp(text)
#     matches = matcher(doc)
#     relationships = []
#     for match_id, start, end in matches:
#         label = nlp.vocab.strings[match_id]  # Get the label (e.g., "ORG" or "PRODUCT")
#         entity_text = doc[start:end].text  # Get the matched text
#         relationships.append((entity_text, label))
#     return relationships

# Function to extract relationships using the specified pattern
def get_relation(sent):
    doc = nlp(sent)
    matcher = Matcher(nlp.vocab)

    # Define the pattern
    pattern = [{'DEP':'ROOT'},
               {'DEP':'prep','OP':"?"},  # Optional preposition
               {'DEP':'agent','OP':"?"},  # Optional agent
               {'POS':'ADJ','OP':"?"}]    # Optional adjective

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

# # df['Relationships'] = df['Processed Sentences'].apply(extract_relationships)
#
# relations = [get_relation(i) for i in tqdm(df['Processed Sentences'])]
#
# print(relations)

# save to csv
df.to_csv('sentences_ner.csv', index=False)
