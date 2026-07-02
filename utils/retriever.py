# from utils.embeddings import load_faiss_index, embed_query


# def retrieve_context(query, top_k=3):
#     """
#     Retrieve the most relevant text chunks for a given query.
#     """

#     # Load FAISS index and stored chunks
#     index, chunks = load_faiss_index()

#     # Convert query to embedding
#     query_embedding = embed_query(query)

#     # Search the FAISS index
#     distances, indices = index.search(query_embedding, top_k)

#     # Get the retrieved chunks
#     retrieved_chunks = []

#     for idx in indices[0]:
#         if idx < len(chunks):
#             retrieved_chunks.append(chunks[idx])

#     return retrieved_chunks
from utils.embeddings import index
import logging


logger = logging.getLogger(__name__)


def _normalize_query_results(results):
    """Normalize various shapes of Upstash index.query results into a list.

    Handles lists, dicts with keys like 'results', 'matches', 'result', and
    objects with a `results` attribute.
    """
    if results is None:
        return []

    # If the client returned an object with a `results` attribute
    if hasattr(results, "results"):
        return list(results.results) or []

    # If it's already a list
    if isinstance(results, list):
        return results

    # If it's a dict, try common keys
    if isinstance(results, dict):
        for key in ("results", "matches", "result", "data", "items"):
            if key in results and results[key] is not None:
                return list(results[key])
        # Fallback: treat the dict itself as a single result
        return [results]

    # Unknown shape: wrap and return
    return [results]


def _extract_text_from_result(r):
    """Extract a textual chunk from a single result entry if possible."""
    # Object-style metadata
    if hasattr(r, "metadata"):
        md = getattr(r, "metadata")
        if isinstance(md, dict) and "text" in md:
            return md["text"]

    # Dict-style result
    if isinstance(r, dict):
        # common metadata containers
        for key in ("metadata", "meta", "payload", "data"):
            md = r.get(key)
            if isinstance(md, dict) and "text" in md:
                return md["text"]
        # direct text field
        for key in ("text", "content", "value"):
            if key in r and isinstance(r[key], str):
                return r[key]

    # Fallback: if the result itself is a string
    if isinstance(r, str):
        return r

    return None


def retrieve_context(query, top_k=3, namespace="default"):
    """
    Retrieve the most relevant chunks for a query using Upstash Vector.
    Upstash embeds `query` server-side with the same model used at upsert time.
    """

    try:
        results = index.query(
            data=query,
            top_k=max(top_k, 5),
            include_metadata=True,
            namespace=namespace,
        )
    except Exception as exc:  # pragma: no cover - defensive runtime error
        logger.exception("Upstash index.query failed: %s", exc)
        return []

    entries = _normalize_query_results(results)

    retrieved_chunks = []
    seen = set()
    for r in entries:
        text = _extract_text_from_result(r)
        if text and text not in seen:
            seen.add(text)
            retrieved_chunks.append(text)

    return retrieved_chunks