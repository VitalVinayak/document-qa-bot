def chunk_documents(documents,
                    chunk_size=1000,
                    overlap=200):

    chunks = []

    for doc in documents:

        text = doc["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "metadata": doc["metadata"]
            })

            start += chunk_size - overlap

    return chunks