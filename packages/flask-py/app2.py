import os
from flask import Flask, request, jsonify
# from flask_cors import CORS
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from rag2 import load_pdfs, train_rag_model, query_rag_model

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
# CORS(app)

# Retrieve the OpenAI API key from the environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Validate that the API key is set
if not openai_api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

# Load the RAG model
model = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)

# Load documents from the data directory
docs = load_pdfs('./data/')
print(f"Loaded {len(docs)} documents")

# Train the RAG model with the loaded documents
rag_chain = train_rag_model(model, docs)

@app.route('/')
def query_root():
    return jsonify({"message": "Welcome to the RAG-based chat API!"})

@app.route('/query', methods=['POST'])
def query_endpoint():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting application/json"}), 400

    query_data = request.get_json()
    query = query_data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        results = query_rag_model(rag_chain, query)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# curl -X POST -H "Content-Type: application/json" -d '{"query": "What is a collection manager?"}' http://localhost:5000/query
if __name__ == '__main__':
    app.run(port=5000, debug=True)
