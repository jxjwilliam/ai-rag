from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
import os
import logging

def load_pdfs(directory):
    logging.info(f"Loading PDFs from directory: {directory}")
    docs = []
    for root, _, files in os.walk(directory):
        if not files:
            logging.warning(f"No files found in directory: {root}")
            continue

        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    loader = PyPDFLoader(file_path)
                    docs.extend(loader.load())
                except Exception as e:
                    logging.warning(f"Error loading PDF file '{file_path}': {e}")
    return docs

def train_rag_model(model, docs):
    logging.info("Training RAG model...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
    chunks = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=model.openai_api_key)
    chroma = Chroma(embedding_function=embeddings, collection_name="my_collection")
    chroma.add_documents(chunks)

    retriever = chroma.as_retriever()

    system_prompt = (
      "You are an assistant for question-answering tasks. "
      "Use the following pieces of retrieved context to answer "
      "the question. If you don't know the answer, say that you "
      "don't know. Use three sentences maximum and keep the "
      "answer concise."
      "\n\n"
      "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(model, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    logging.info("RAG model trained successfully.")
    return rag_chain

def query_rag_model(rag_chain, query):
    logging.info(f"Querying RAG model with input: {query}")
    results = rag_chain({"input": query})["result"]
    logging.info(f"Query results: {results}")
    return results
