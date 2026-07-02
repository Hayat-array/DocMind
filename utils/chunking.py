# from langchain.text_splitter import RecursiveCharacterTextSplitter


# def create_chunks(text, chunk_size=500, chunk_overlap=100):
#     """
#     Splits the extracted text into smaller overlapping chunks.
#     """

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         separators=["\n\n", "\n", ".", " ", ""]
#     )

#     chunks = splitter.split_text(text)

#     return chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(text, chunk_size=1000, chunk_overlap=150):
    """
    Splits the extracted text into smaller overlapping chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", ".", " ", ""]
    )

    chunks = [chunk.strip() for chunk in splitter.split_text(text) if chunk.strip()]

    return chunks