from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader

def envs():
  if os.path.exists('.env'):
    load_dotenv()


def load_pdfs(directory):
    docs = []
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)
        if os.path.isfile(entry_path) and entry_path.endswith(".pdf"):
            loader = PyPDFLoader(entry_path)
            docs.extend(loader.load())
        elif os.path.isdir(entry_path):
            docs.extend(load_pdfs(entry_path))
    return docs

