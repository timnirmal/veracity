from py2neo import Graph
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
from py2neo import Graph
import igraph as ig

# Connect to Neo4j
uri = "neo4j+s://b8d08542.databases.neo4j.io"  # Replace with your URI
username = "neo4j"              # Replace with your username
password = "6aGLLE1wrWr4pGornnwPnhHys6MU2Ag4pSO8SeFSc2I"           # Replace with your password
graph = Graph(uri, auth=(username, password))
#
# # Fetch nodes and relationships
# query = """
# MATCH (e1:Entity)-[r:RELATION]->(e2:Entity)
# RETURN e1.name, type(r), r.name, e2.name
# """
# data = graph.run(query)
#
# # Create a NetworkX graph
# G = nx.MultiDiGraph()
#
# # Add nodes and edges to the NetworkX graph
# for e1, rel_type, rel_name, e2 in data:
#     G.add_node(e1)
#     G.add_node(e2)
#     G.add_edge(e1, e2, label=rel_name)
#
# # Draw the graph
# pos = nx.spring_layout(G)  # positions for all nodes
# nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=15)
#
# # Draw edge labels
# edge_labels = nx.get_edge_attributes(G, 'label')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
#
# # Show the plot
# plt.show()
#
# # save
# plt.savefig('graph.png')
#
# Fetch nodes and relationships
query = """
MATCH (e1:Entity)-[r:RELATION]->(e2:Entity)
RETURN e1.name AS source, type(r) AS type, r.name AS relation, e2.name AS target
"""
data = graph.run(query)

# Create an igraph graph
G = ig.Graph(directed=True)

# Create a mapping of node names to indices
node_mapping = {}
for source, _, relation, target in data:
    for node in [source, target]:
        if node not in node_mapping:
            node_mapping[node] = len(node_mapping)
            G.add_vertex(name=node)

# Add edges to the graph
for source, _, relation, target in data:
    G.add_edge(node_mapping[source], node_mapping[target], label=relation)

# Plot the graph
layout = G.layout("kk")  # Kamada-Kawai layout
ig.plot(G, layout=layout, vertex_label=G.vs["name"], edge_label=G.es["label"], margin=80)