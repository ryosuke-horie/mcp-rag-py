# rag_core/vectordb/storage.py
import duckdb
import numpy as np
from typing import List, Tuple

class DuckDBVectorStore:
    """
    A vector store implementation using DuckDB with the VSS extension.
    """
    def __init__(self, db_path: str = "vector_store.db", table_name: str = "embeddings"):
        """
        Initializes the DuckDBVectorStore.

        Args:
            db_path (str): Path to the DuckDB database file.
            table_name (str): Name of the table to store embeddings.
        """
        self.db_path = db_path
        self.table_name = table_name
        self.embedding_dim = 1024  # Dimension for bge-m3

        try:
            self.conn = duckdb.connect(database=self.db_path, read_only=False)
            # Install and load VSS extension if not already done
            self.conn.execute("INSTALL vss;")
            self.conn.execute("LOAD vss;")
            # Create table if it doesn't exist
            self._create_table()
        except Exception as e:
            print(f"Error initializing DuckDBVectorStore: {e}")
            raise

    def _create_table(self):
        """Creates the embedding table if it doesn't exist."""
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            text VARCHAR,
            embedding FLOAT[{self.embedding_dim}]
        );
        """
        try:
            self.conn.execute(create_table_sql)
        except Exception as e:
            print(f"Error creating table: {e}")
            raise

    def add_embeddings(self, texts: List[str], embeddings: List[List[float]]):
        """
        Adds text chunks and their corresponding embeddings to the store.

        Args:
            texts (List[str]): List of text chunks.
            embeddings (List[List[float]]): List of corresponding embeddings (lists of floats).
        """
        if len(texts) != len(embeddings):
            raise ValueError("Number of texts and embeddings must match.")
        if not embeddings:
            print("No embeddings provided to add.")
            return

        # Get the next available ID
        try:
            max_id = self.conn.execute(f"SELECT COALESCE(MAX(id), 0) FROM {self.table_name}").fetchone()[0]
        except Exception:
            max_id = 0

        # Use parameterized query for safe insertion
        insert_sql = f"INSERT INTO {self.table_name} (id, text, embedding) VALUES (?, ?, ?)"

        try:
            self.conn.begin() # Start transaction
            # Insert data row by row with manually managed IDs
            for i, (text, embedding) in enumerate(zip(texts, embeddings), start=1):
                self.conn.execute(insert_sql, [max_id + i, text, embedding])
            self.conn.commit() # Commit changes if all insertions succeed
            print(f"Successfully added {len(texts)} embeddings.")
        except Exception as e:
            print(f"Error adding embeddings: {e}")
            self.conn.rollback() # Rollback on error
            raise
        # No finally block needed as connection closing is handled in `close` method

    def similarity_search(self, query_embedding: List[float], k: int = 5) -> List[Tuple[str, float]]:
        """
        Performs similarity search using cosine similarity.

        Args:
            query_embedding (List[float]): The query embedding (list of floats).
            k (int): Number of nearest neighbors to retrieve.

        Returns:
            List[Tuple[str, float]]: List of (text, similarity_score) tuples.
        """
        # Optional: Add a check for the length of the list if needed
        # if len(query_embedding) != self.embedding_dim:
        #     raise ValueError(f"Query embedding dimension mismatch. Expected {self.embedding_dim}, got {len(query_embedding)}")

        # Use array_distance for cosine similarity (1 - cosine distance)
        # Note: VSS uses list_similarity for cosine similarity directly in newer versions,
        # but array_distance is generally available. Cosine Similarity = 1 - Cosine Distance
        search_sql = f"""
        SELECT text, array_cosine_similarity(embedding, ?::FLOAT[1024]) AS similarity
        FROM {self.table_name}
        ORDER BY similarity DESC
        LIMIT ?;
        """
        try:
            results = self.conn.execute(search_sql, [query_embedding, k]).fetchall()
            # Convert results to desired format (text, score)
            # fetchall returns list of tuples, e.g., [('doc1 text', 0.98), ('doc2 text', 0.95)]
            return results
        except Exception as e:
            print(f"Error during similarity search: {e}")
            return []

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("DuckDB connection closed.")

import os # Add import for os module

# Example Usage (Optional - for testing)
if __name__ == '__main__':
    db_file = "test_vector_store.db"
    # Ensure a clean state by removing the old DB file if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing database file: {db_file}")

    # Example: Initialize store
    store = DuckDBVectorStore(db_path=db_file, table_name="test_embeddings")

    # Example: Add embeddings
    texts_to_add = ["This is the first document.", "This document is about ducks.", "A third example document."]
    # Dummy embeddings (replace with actual embeddings from your model)
    dummy_embeddings = [np.random.rand(1024).astype(np.float32) for _ in texts_to_add]
    store.add_embeddings(texts_to_add, dummy_embeddings)

    # Example: Similarity search
    query_vec = np.random.rand(1024).astype(np.float32)
    similar_docs = store.similarity_search(query_vec, k=2)
    print("\nSimilarity Search Results:")
    for text, score in similar_docs:
        print(f"Score: {score:.4f} - Text: {text}")

    # Clean up
    store.close()
    # os.remove(db_file) # Keep commented out, removal is now at the start
    # print("Test database file removed.")
