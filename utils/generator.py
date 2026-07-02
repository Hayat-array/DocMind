import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, context_chunks):
    """
    Generate an answer using the retrieved context.
    """

    # Combine retrieved chunks with labels so the model can anchor each claim.
    context_lines = []
    for index, chunk in enumerate(context_chunks, start=1):
        context_lines.append(f"Chunk {index}: {chunk}")

    context = "\n\n".join(context_lines)

    prompt = f"""You are a precise document QA assistant.

Use only the context below. Do not guess, and do not add outside facts.

If the context does not contain the answer, reply exactly:
I couldn't find the answer in the provided document.

When the context supports the answer, write a short, direct response.

Context:
{context}

Question:
{question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You answer questions only from the provided document context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.0,
        max_tokens=256
    )

    answer = response.choices[0].message.content

    return answer