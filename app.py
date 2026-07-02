import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from utils.pdf_loader import load_pdf
from utils.chunking import create_chunks
from utils.embeddings import save_faiss_index
from utils.retriever import retrieve_context
from utils.generator import generate_answer

app = Flask(__name__)

UPLOAD_FOLDER = "documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():

    answer = ""
    retrieved_context = []
    upload_message = ""
    question = ""

    if request.method == "POST":

        # Upload PDF
        if "pdf" in request.files:

            file = request.files["pdf"]

            if file.filename != "":

                filename = secure_filename(file.filename)

                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )

                file.save(filepath)

                # Extract text
                text = load_pdf(filepath)

                # Split into chunks
                chunks = create_chunks(text)

                # Create FAISS database
                save_faiss_index(chunks)

                upload_message = "✅ PDF uploaded and indexed successfully."

        # Ask Question
        question = request.form.get("question")

        if question:

            retrieved_context = retrieve_context(question)

            answer = generate_answer(
                question,
                retrieved_context
            )

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        context=retrieved_context,
        upload_message=upload_message
    )


if __name__ == "__main__":
    app.run(debug=True)