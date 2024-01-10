import openai
from openai import OpenAI

api_key = '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'


def chat_with_openai(api_key, initial_message=None):
    client = OpenAI(api_key=api_key)

    messages = []

    if initial_message:
        messages.append({"role": "user", "content": initial_message})

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})

        # Send the query to GPT-3.5 and get the response
        full_response = ""
        for response in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")

        # Assuming the response is a Cypher query, execute it in Neo4j
        cypher_query = full_response.strip()
        neo4j_results = execute_cypher_query(
            cypher_query)  # This function needs to be defined as shown in the previous example
        formatted_results = format_neo4j_results(neo4j_results)  # Format the results into a readable format

        print("Assistant:", formatted_results)
        messages.append({"role": "assistant", "content": formatted_results})



from neo4j import GraphDatabase

uri = "neo4j+s://b8d08542.databases.neo4j.io"  # Replace with your URI
username = "neo4j"  # Replace with your username
password = "6aGLLE1wrWr4pGornnwPnhHys6MU2Ag4pSO8SeFSc2I"  # Replace with your password
driver = GraphDatabase.driver(uri, auth=(username, password))


def execute_cypher_query(cypher_query):
    with driver.session() as session:
        results = session.run(cypher_query)
        return [record for record in results]





# # Example usage
# question = "What is this paper about"
# result = process_question(question)
# print(result)


def format_neo4j_results(results):
    # Implement formatting logic here
    # This could be as simple as concatenating result values or more complex formatting depending on your data
    return '\n'.join([str(result) for result in results])


if __name__ == "__main__":
    chat_with_openai(api_key)
