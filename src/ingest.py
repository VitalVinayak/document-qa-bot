import chromadb
from sentence_transformers import SentenceTransformer

from document_loader import load_documents
from chunker import chunk_documents

# Load documents
docs = load_documents()

# Create chunks
chunks = chunk_documents(docs)

# Create embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Create ChromaDB client
client = chromadb.PersistentClient(path="db")

collection = client.get_or_create_collection("rag_docs")

# Generate embeddings
embeddings = embedding_model.encode(
    [chunk["text"] for chunk in chunks]
).tolist()

# Store in ChromaDB
collection.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=[chunk["text"] for chunk in chunks],
    metadatas=[chunk["metadata"] for chunk in chunks],
    embeddings=embeddings
)

print("Documents indexed successfully!")