import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, create_retrieval_chain

import logging

def load_pdfs(directory):
    docs = []
    for root, _, files in os.walk(directory):
      if not files:
        print(f"No files in {root}")
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

def load_pdfs_1(directory):
    docs = []
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)
        if os.path.isfile(entry_path) and entry_path.endswith(".pdf"):
            loader = PyPDFLoader(entry_path)
            docs.extend(loader.load())
        elif os.path.isdir(entry_path):
            docs.extend(load_pdfs(entry_path))
    return docs


def train_rag_model_1(model, docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    chunks = text_splitter.split_documents(docs)
    print(f"Number of chunks: {len(chunks)}", model.openai_api_key)

    embeddings = OpenAIEmbeddings(model="gpt-4o", openai_api_key=model.openai_api_key)
    chroma = Chroma(embedding_function=embeddings, collection_name="my_collection")

    chroma.add_documents(chunks)

    rag_chain = create_retrieval_chain(chroma, model=model)
    return rag_chain

def train_rag_model(model, docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
    chunks = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="gpt-4o", openai_api_key=model.openai_api_key)
    chroma = Chroma(embedding_function=embeddings, collection_name="my_collection")

    chroma.add_documents(chunks)

    model = ChatOpenAI(model="gpt-4o", openai_api_key=model.openai_api_key)
    rag_chain = RetrievalQA(retriever=chroma.as_retriever(), llm=model)
    return rag_chain

def query_rag_model(rag_chain, query):
    results = rag_chain({"query": query})
    return results


def query_rag_model(rag_chain, query):
    results = rag_chain.invoke({"input": query})
    return results
