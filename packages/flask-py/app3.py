from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Import the functions from the notebook
from rag3 import load_pdfs, train_rag_model, generate_rag_log

pdf_dir = 'data'
docs = load_pdfs(pdf_dir)
rag_chain = train_rag_model(docs)

@app.route('/generate-rag-log', methods=['POST'])
def generate_log():
    input_text = request.json.get('input')
    if not input_text:
        return jsonify({"error": "No input text provided"}), 400
    result = generate_rag_log(input_text, rag_chain)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
