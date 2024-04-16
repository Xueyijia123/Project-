from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI

import requests

query_gen_str = """\
You are a helpful assistant that generates multiple search queries based on a \
single input query. Generate {num_queries} search queries, one on each line, \
related to the following input query:
Query: {query}
Queries:
"""

def generate_queries(query: str, model_url: str, num_queries: int = 4):
    try:
        # Format the prompt with the actual query and number of queries
        prompt = query_gen_str.format(query=query, num_queries=num_queries)
        
        # Prepare the payload for the POST request
        data = {
            'prompt': prompt,
            'temperature': 0.7,  # You can adjust this value as needed
            'max_tokens': 100,  # Adjust based on how long you expect the output to be
        }
        
        # Make the POST request to your model's API endpoint
        response = requests.post(model_url, json=data)

        response.raise_for_status()

        response_json = response.json()

        queries = response_json.get('choices', [])[0].get('text', '').split("\n")

        queries = [q for q in queries if q.strip() != '']

        queries_str = "\n".join(queries)
        print(f"Generated queries:\n{queries_str}")
        return queries
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example use of the function
model_url = 'https://dvo12utveqd-496ff2e9c6d22116-8000-colab.googleusercontent.com/'  # model endpoint
sample_query = "climate change effects"
generated_queries = generate_queries(sample_query, model_url, num_queries=4)

# Output the generated queries
for q in generated_queries:
    print(q)