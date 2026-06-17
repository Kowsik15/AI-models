from flask import Flask, render_template, request, jsonify
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global Vector DB
vector_db = None

# Embedding Model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Local LLM
llm = OllamaLLM(
    model="llama3"
)

# ----------------------------------
# Process Uploaded PDF
# ----------------------------------

def process_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    db = FAISS.from_documents(
        chunks,
        embedding_model
    )

    return db

# ----------------------------------
# Ask Question
# ----------------------------------

def ask_rag(query):

    global vector_db

    if vector_db is None:
        return "Please upload a PDF first."

    results = vector_db.similarity_search(
        query,
        k=5
    )

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    prompt = f"""
You are a friendly and knowledgeable teacher.

Answer the question using ONLY the information provided in the context.

Instructions:
1. Start with a short introduction.
2. Explain every concept point by point.
3. For each point use the format:

Point 1:
- Explanation:
- Why it is important:
- Example:

Point 2:
- Explanation:
- Why it is important:
- Example:

4. Use simple language suitable for beginners.
5. Do not copy text directly from the context.
6. Explain in your own words.
7. If information is not available in the context, say:
   "I could not find that information in the uploaded document."

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response

# ----------------------------------
# Home Page
# ----------------------------------

@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------------
# Upload PDF
# ----------------------------------

@app.route("/upload", methods=["POST"])
def upload_pdf():

    global vector_db

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({
            "message": "No file selected"
        })

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)

    vector_db = process_pdf(file_path)

    return jsonify({
        "message": "PDF uploaded successfully"
    })

# ----------------------------------
# Chat Route
# ----------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data["question"]

    answer = ask_rag(question)

    return jsonify({
        "answer": answer
    })

# ----------------------------------
# Run App
# ----------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )