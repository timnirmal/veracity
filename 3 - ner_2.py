import pandas as pd
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")

# Function to extract named entities
def extract_named_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Function to extract relationships
def get_relation(sent):
    doc = nlp(sent)
    matcher = Matcher(nlp.vocab)

    # Define the pattern
    pattern = [{'DEP': 'ROOT'}, {'DEP': 'prep', 'OP': "?"},
               {'DEP': 'agent', 'OP': "?"}, {'POS': 'ADJ', 'OP': "?"}]

    matcher.add("relationship_pattern", [pattern])
    matches = matcher(doc)
    return [doc[start:end].text for match_id, start, end in matches]

# Function to associate entities with relationships
def find_entity_relationships(sentence):
    entities = extract_named_entities(sentence)
    relationships = get_relation(sentence)
    entity_relations = []

    for rel in relationships:
        rel_span = nlp(rel).text
        for i in range(len(entities) - 1):
            for j in range(i + 1, len(entities)):
                entity1, entity2 = entities[i][0], entities[j][0]
                # Example: [(Entity1, Relation, Entity2)]
                entity_relations.append((entity1, rel_span, entity2))

    return entity_relations

# Load your data
df = pd.read_csv('sentences_processed.csv')

# Apply the function to your data
df['Entity_Relations'] = df['Processed Sentences'].apply(find_entity_relationships)

# Save to CSV
df.to_csv('sentences_entity_relations.csv', index=False)


# 6aGLLE1wrWr4pGornnwPnhHys6MU2Ag4pSO8SeFSc2I
# Username: neo4j