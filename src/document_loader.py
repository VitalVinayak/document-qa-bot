import os
from pypdf import PdfReader
from docx import Document

def extract_pdf(file_path):
    pages = []

    reader = PdfReader(file_path)

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append({
                "text": text,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": i + 1
                }
            })

    return pages


def extract_docx(file_path):
    doc = Document(file_path)

    text = "\n".join([p.text for p in doc.paragraphs])

    return [{
        "text": text,
        "metadata": {
            "source": os.path.basename(file_path),
            "page": 1
        }
    }]


def load_documents(folder="data"):
    documents = []

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if file.endswith(".pdf"):
            documents.extend(extract_pdf(path))

        elif file.endswith(".docx"):
            documents.extend(extract_docx(path))

    return documents