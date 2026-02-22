import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_DIR = "data"
FAISS_DIR = "faiss_index"


def load_documents():
    documents = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_DIR, file), encoding="utf-8")
            documents.extend(loader.load())

    return documents


def build_faiss():
    print("📚 Loading documents...")
    documents = load_documents()

    print("✂ Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,     # Bigger chunk = better context
        chunk_overlap=100    # Reduced overlap to prevent duplication
    )

    docs = text_splitter.split_documents(documents)

    print("🔎 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("🧠 Building FAISS index...")
    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local(FAISS_DIR)

    print("✅ FAISS index created successfully!")


if __name__ == "__main__":
    build_faiss()