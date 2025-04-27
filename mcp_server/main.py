# FastAPI application entry point for MCP server
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "MCP RAG Server"}

# Add endpoints to interact with rag_core components here
