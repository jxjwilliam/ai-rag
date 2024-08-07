from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rag1 import create_rag_model

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RAG model
rag_chain = create_rag_model()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    query = data['query']
    history = data.get('history', [])
    response = rag_chain.invoke({"input": query})
    return {"response": response}
