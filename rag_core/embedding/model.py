# Embedding model implementation using Ollama
from langchain_ollama import OllamaEmbeddings # Updated import
import os
from typing import List

def initialize_embedding_model(
    ollama_base_url: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
    model_name: str = os.environ.get("EMBEDDING_MODEL_NAME", "bge-m3")
) -> OllamaEmbeddings:
    """
    Initializes and returns the Ollama embedding model instance.

    Reads the Ollama base URL and model name from environment variables
    with default values.

    Args:
        ollama_base_url (str): The base URL of the Ollama server.
                               Defaults to "http://localhost:11434" or OLLAMA_BASE_URL env var.
        model_name (str): The name of the embedding model to use.
                          Defaults to "bge-m3" or EMBEDDING_MODEL_NAME env var.

    Returns:
        OllamaEmbeddings: An instance of the Ollama embedding model.
    """
    print(f"Initializing Ollama Embeddings with base_url='{ollama_base_url}' and model='{model_name}'")
    embeddings = OllamaEmbeddings(base_url=ollama_base_url, model=model_name)
    return embeddings

def embed_texts(texts: List[str], embeddings: OllamaEmbeddings) -> List[List[float]]:
    """
    Embeds a list of texts using the provided Ollama embedding model.

    Args:
        texts (List[str]): A list of texts to embed.
        embeddings (OllamaEmbeddings): The initialized Ollama embedding model instance.

    Returns:
        List[List[float]]: A list of embedding vectors, one for each input text.
    """
    print(f"Embedding {len(texts)} documents...")
    embedded_vectors = embeddings.embed_documents(texts)
    print("Embedding complete.")
    return embedded_vectors

def embed_query(text: str, embeddings: OllamaEmbeddings) -> List[float]:
    """
    Embeds a single query text using the provided Ollama embedding model.

    Args:
        text (str): The query text to embed.
        embeddings (OllamaEmbeddings): The initialized Ollama embedding model instance.

    Returns:
        List[float]: The embedding vector for the input query text.
    """
    print(f"Embedding query: '{text[:50]}...'") # Log first 50 chars
    embedded_vector = embeddings.embed_query(text)
    print("Query embedding complete.")
    return embedded_vector

# Example usage (optional, for testing purposes)
if __name__ == '__main__':
    # Ensure Ollama server is running and the model is available
    # Example: ollama run bge-m3

    # Set environment variables if needed (or rely on defaults)
    # os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    # os.environ["EMBEDDING_MODEL_NAME"] = "bge-m3"

    try:
        print("--- Testing Embedding Model ---")
        embedding_model = initialize_embedding_model()

        # Test embedding documents
        sample_texts = [
            "This is the first document.",
            "This document is the second document.",
            "And this is the third one.",
            "Is this the first document?",
        ]
        vectors = embed_texts(sample_texts, embedding_model)
        print(f"Generated {len(vectors)} vectors.")
        if vectors:
            print(f"Dimension of the first vector: {len(vectors[0])}")
            # print("First vector (first 10 dims):", vectors[0][:10]) # Uncomment to see part of the vector

        print("\n--- Testing Query Embedding ---")
        # Test embedding a query
        query = "What is the second document about?"
        query_vector = embed_query(query, embedding_model)
        print(f"Generated query vector with dimension: {len(query_vector)}")
        # print("Query vector (first 10 dims):", query_vector[:10]) # Uncomment to see part of the vector

        print("\n--- Embedding Test Successful ---")

    except Exception as e:
        print(f"\n--- Embedding Test Failed ---")
        print(f"An error occurred: {e}")
        print("Please ensure the Ollama server is running and the specified model ('bge-m3' by default) is available.")
        print("You might need to run 'ollama run bge-m3' in your terminal.")
