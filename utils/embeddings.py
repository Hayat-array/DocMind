# # import os
# # import pickle
# # import faiss
# # import numpy as np
# # from sentence_transformers import SentenceTransformer

# # # Load embedding model only once
# # model = SentenceTransformer("all-MiniLM-L6-v2")


# # def create_embeddings(chunks):
# #     """
# #     Convert text chunks into embeddings.
# #     """
# #     embeddings = model.encode(chunks)
# #     return np.array(embeddings, dtype="float32")


# # def save_faiss_index(chunks, index_path="database/faiss_index"):
# #     """
# #     Create a FAISS index and save it along with the text chunks.
# #     """

# #     embeddings = create_embeddings(chunks)

# #     dimension = embeddings.shape[1]

# #     index = faiss.IndexFlatL2(dimension)
# #     index.add(embeddings)

# #     os.makedirs("database", exist_ok=True)

# #     faiss.write_index(index, index_path)

# #     with open(index_path + "_texts.pkl", "wb") as f:
# #         pickle.dump(chunks, f)

# #     print("✅ FAISS index saved successfully.")


# # def load_faiss_index(index_path="database/faiss_index"):
# #     """
# #     Load the saved FAISS index and corresponding text chunks.
# #     """

# #     index = faiss.read_index(index_path)

# #     with open(index_path + "_texts.pkl", "rb") as f:
# #         chunks = pickle.load(f)

# #     return index, chunks


# # def embed_query(query):
# #     """
# #     Convert a user query into an embedding.
# #     """

# #     embedding = model.encode([query])

# #     return np.array(embedding, dtype="float32")

# import os
# from upstash_vector import Index

# # Reads UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN from env
# index = Index.from_env()


# def save_faiss_index(chunks, namespace="default"):
#     """
#     Upserts text chunks into Upstash Vector.
#     Upstash embeds the raw text server-side using the index's built-in
#     embedding model (set when you create the index in the Upstash console —
#     e.g. mixedbread-ai/mxbai-embed-large-v1 or BAAI/bge-large-en-v1.5).

#     Kept the same function name as before so app.py doesn't need changes.
#     """

#     # Clear old vectors for this doc/session before inserting new ones
#     index.reset(namespace=namespace)

#     vectors = [
#         (str(i), chunk, {"text": chunk})
#         for i, chunk in enumerate(chunks)
#     ]

#     # Upstash batches internally; 100/request is a safe chunk size
#     batch_size = 100
#     for start in range(0, len(vectors), batch_size):
#         index.upsert(vectors=vectors[start:start + batch_size], namespace=namespace)

#     print(f"✅ {len(chunks)} chunks upserted to Upstash Vector.")


# def load_faiss_index(namespace="default"):
#     """
#     No-op placeholder kept for compatibility with retriever.py's old import.
#     Upstash has no local index/pickle to load — retrieval happens via query().
#     """
#     return index, namespace


# def embed_query(query):
#     """
#     No-op placeholder — Upstash embeds the query text server-side too,
#     so retriever.py just passes the raw string to index.query().
#     """
#     return query

import os
from dotenv import load_dotenv
from upstash_vector import Index

load_dotenv()

# Reads UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN from env
index = Index.from_env()


def save_faiss_index(chunks, namespace="default"):
    """
    Upserts text chunks into Upstash Vector.
    Upstash embeds the raw text server-side using the index's built-in
    embedding model (set when you create the index in the Upstash console —
    e.g. mixedbread-ai/mxbai-embed-large-v1 or BAAI/bge-large-en-v1.5).

    Kept the same function name as before so app.py doesn't need changes.
    """

    # Clear old vectors for this doc/session before inserting new ones
    index.reset(namespace=namespace)

    vectors = [
        (str(i), chunk, {"text": chunk})
        for i, chunk in enumerate(chunks)
    ]

    # Upstash batches internally; 100/request is a safe chunk size
    batch_size = 100
    for start in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[start:start + batch_size], namespace=namespace)

    print(f"✅ {len(chunks)} chunks upserted to Upstash Vector.")


def load_faiss_index(namespace="default"):
    """
    No-op placeholder kept for compatibility with retriever.py's old import.
    Upstash has no local index/pickle to load — retrieval happens via query().
    """
    return index, namespace


def embed_query(query):
    """
    No-op placeholder — Upstash embeds the query text server-side too,
    so retriever.py just passes the raw string to index.query().
    """
    return query