import re
import chromadb
from sentence_transformers import SentenceTransformer

# Connect to ChromaDB
client = chromadb.PersistentClient(path="db")
collection = client.get_collection("rag_docs")

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def clean_text(text):
    # Remove extra spaces and newlines
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)

    # Remove repeated spaces
    text = text.strip()

    return text


def ask_question(question):

    query_embedding = embedding_model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2,
        include=["documents", "metadatas", "distances"]
    )

    # Reject unrelated questions
    if results["distances"][0][0] > 1.2:
        return "I cannot find the answer in the documents.", []

    answer = ""
    citations = []

    for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0]):

        cleaned_doc = clean_text(doc)

        answer += cleaned_doc + "\n\n"

        citations.append(
            f"{meta['source']} - Page {meta['page']}"
        )

    return answer, citations