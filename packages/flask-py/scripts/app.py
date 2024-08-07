from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import langchain
from langchain.chains import RetrivalQA

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat_with_ai(query: str):
    # Example Langchain usage for AI chat
    response = langchain.some_function(query)
    return {"response": response}

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    query = data['query']
    history = data.get('history', [])
    response = chat_with_pdf(query, history)
    return {"response": response}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    # Process the PDF content using Langchain
    analysis = langchain.analyze_pdf(content)
    return {"analysis": analysis}

@app.post("/chat-with-pdf")
async def chat_with_pdf(query: str):
    # Use Langchain for RAG-based chat with the analyzed PDF content
    response = langchain.chat_with_pdf(query)
    return {"response": response}
