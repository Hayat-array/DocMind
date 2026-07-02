HEAD
# DocMind

DocMind is a Flask-based Retrieval-Augmented Generation (RAG) app that lets you upload a PDF and ask questions about its contents.

## Features

- PDF upload and text extraction
- Chunking and vector indexing with Upstash Vector
- Context-aware question answering with Groq
- Clean chat-style UI with theme toggle
- Collapsible retrieved context for debugging and transparency

## Tech Stack

- Python
- Flask
- Upstash Vector
- Groq
- LangChain text splitters
- HTML, CSS, and JavaScript

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your keys:

```env
GROQ_API_KEY=your_groq_api_key
UPSTASH_VECTOR_REST_URL=your_upstash_vector_rest_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_vector_rest_token
```

4. Run the app:

```bash
py -3 app.py
```

5. Open the local server in your browser and upload a PDF.

## How It Works

1. Upload a PDF.
2. The app extracts text and splits it into chunks.
3. Chunks are stored in Upstash Vector.
4. When you ask a question, the most relevant chunks are retrieved.
5. Groq generates an answer grounded in that retrieved context.

## Notes

- The app is designed to answer from the uploaded document only.
- If the answer is not in the document, it will say so instead of guessing.
=======
# DocMind

