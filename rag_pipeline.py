import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

FAISS_DIR = "faiss_index"


# -----------------------
# Load Vector Store
# -----------------------

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        FAISS_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )


vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 6}  # retrieve more relevant chunks
)


# -----------------------
# LLM Setup
# -----------------------

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",  # stable Groq model
    temperature=0
)


# -----------------------
# Prompt Template
# -----------------------

prompt = ChatPromptTemplate.from_template("""
You are an official assistant for NIT Trichy (NITT).

Use ONLY the provided context to answer.
If information is not found in the context, say:
"I could not find this information on the NITT website."

Avoid repeating names or sentences.
Summarize clearly and professionally.

Context:
{context}

Question:
{question}

Answer:
""")


# -----------------------
# RAG Pipeline
# -----------------------

def ask_question(question: str):

    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "context": context,
        "question": question
    })