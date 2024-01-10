import ast

import pandas as pd
from neo4j import GraphDatabase

uri = "neo4j+s://b8d08542.databases.neo4j.io"  # Replace with your URI
username = "neo4j"              # Replace with your username
password = "6aGLLE1wrWr4pGornnwPnhHys6MU2Ag4pSO8SeFSc2I"           # Replace with your password

driver = GraphDatabase.driver(uri, auth=(username, password))

df = pd.read_csv('sentences_entity_relations.csv')

# def add_relationship(tx, entity1, entity2, relationship):
#     tx.run("MERGE (a:Entity {name: $entity1}) "
#            "MERGE (b:Entity {name: $entity2}) "
#            "MERGE (a)-[r:RELATIONSHIP {type: $relationship}]->(b)",
#            entity1=entity1, entity2=entity2, relationship=relationship)

def add_entity_relation(tx, entity1, relation, entity2):
    query = (
        "MERGE (e1:Entity {name: $entity1}) "
        "MERGE (e2:Entity {name: $entity2}) "
        "MERGE (e1)-[r:RELATION {name: $relation}]->(e2)"
    )
    tx.run(query, entity1=entity1, relation=relation, entity2=entity2)


# with driver.session() as session:
#     for index, row in df.iterrows():
#         # Assuming 'Entity1', 'Entity2', and 'Relationship' are columns in your df
#         session.write_transaction(add_relationship, row['Entity1'], row['Entity2'], row['Relationship'])

# with driver.session() as session:
#     for _, row in df.iterrows():
#         if row['Entity_Relations'] != '[]':
#             for entity_relation in row['Entity_Relations']:
#                 print(row['Entity_Relations'])  # [('1', 'Hallacy', 'Chris Hallacy'), ('1', 'Hallacy', '1')
#                 entity1, relation, entity2 = row['Entity_Relations']
#                 session.write_transaction(add_entity_relation, entity1, relation, entity2)

with driver.session() as session:
    for _, row in df.iterrows():
        # Convert string representation to list of tuples
        try:
            entity_relations = ast.literal_eval(row['Entity_Relations'])
        except (ValueError, SyntaxError):
            continue  # Skip rows where conversion fails

        for entity_relation in entity_relations:
            try:
                entity1, relation, entity2 = entity_relation
                print(entity1, relation, entity2)
                session.write_transaction(add_entity_relation, entity1, relation, entity2)
            except ValueError:
                continue  # Skip malformed tuples

driver.close()
