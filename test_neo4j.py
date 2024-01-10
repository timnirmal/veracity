from neo4j import GraphDatabase

# Neo4j connection credentials
uri = "neo4j+s://b8d08542.databases.neo4j.io"  # Replace with your URI
username = "neo4j"  # Replace with your username
password = "6aGLLE1wrWr4pGornnwPnhHys6MU2Ag4pSO8SeFSc2I"  # Replace with your password

# Create a driver instance
driver = GraphDatabase.driver(uri, auth=(username, password))


def execute_cypher_query(cypher_query):
    """
    Executes a Cypher query and returns the results.
    """
    with driver.session() as session:
        results = session.run(cypher_query)
        return [record for record in results]


def format_neo4j_results(results):
    """
    Formats Neo4j results into a readable format.
    """
    return '\n'.join([str(result) for result in results])


def main():
    """
    Main function to execute a test Cypher query.
    """
    # Define a test Cypher query
    test_query = "MATCH (n) RETURN n LIMIT 10"  # Modify this query based on your Neo4j data model

    # Execute the test query
    test_results = execute_cypher_query(test_query)

    # Format and print the results
    formatted_results = format_neo4j_results(test_results)
    print("Test Query Results:\n", formatted_results)


if __name__ == "__main__":
    main()
