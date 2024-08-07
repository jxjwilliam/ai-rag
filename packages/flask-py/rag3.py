import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs(directory):
    docs = []
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)
        if os.path.isfile(entry_path) and entry_path.endswith('.pdf'):
            loader = PyPDFLoader(entry_path)
            docs.extend(loader.load())
    return docs


from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain

def train_rag_model(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
    chunks = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="gpt-4o")
    chroma = Chroma(embedding_function=embeddings, collection_name="my_collection")

    chroma.add_documents(chunks)

    rag_chain = create_retrieval_chain(chroma, model="gpt-4o")
    return rag_chain

