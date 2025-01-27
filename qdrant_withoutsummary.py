from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF
import os
from docx import Document

# Initializing the sentence transformer model
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Functions to extract content from PDF and DOCX files
def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    content_dict = {}
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        content_dict[f"Page {page_num + 1}"] = page_text
    return content_dict

def extract_docx_content(docx_path):
    doc = Document(docx_path)
    content_dict = {}
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    content_dict["Page 1"] = "\n".join(full_text)
    return content_dict

def extract_contents_from_directory(directory_path):
    labeled_dict = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            content_dict = extract_pdf_content(file_path)
            labeled_dict[filename] = content_dict
        elif filename.endswith(".docx"):
            file_path = os.path.join(directory_path, filename)
            content_dict = extract_docx_content(file_path)
            labeled_dict[filename] = content_dict
    return labeled_dict

# Specifying the directory containing your PDF and Word documents
directory_path = os.path.expanduser('~/Documents/qdrant')
documents = extract_contents_from_directory(directory_path)

# Setting up the Qdrant client and collection
client = QdrantClient(":memory:")

# Check and create collection as needed
if client.collection_exists(collection_name="local_files"):
    client.delete_collection(collection_name="local_files")
client.create_collection(
    collection_name="local_files",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE,
    ),
)

# Prepare and upload points
points_to_upload = []
point_id = 0
for document_name, pages in documents.items():
    for page, text in pages.items():
        vector = encoder.encode(text).tolist()
        points_to_upload.append(models.PointStruct(
            id=point_id,
            vector=vector,
            payload={"doc": document_name, "page": page, "text": text}
        ))
        point_id += 1

client.upload_points(
    collection_name="local_files",
    points=points_to_upload
)

# User input and search
your_query_here = input("What are you looking for? ")
hits = client.search(
    collection_name="local_files",
    query_vector=encoder.encode(your_query_here).tolist(),
    #EDIT THE NUMBER BELOW TO INCREASE THE NUMBER OF SEARCH RESULTS:
    limit=1
)

# Display search results
for hit in hits:
    print(f"What you're looking for can be found in {hit.payload['doc']}, on {hit.payload['page']}.")
    print(f"Here's what was relevant: {hit.payload['text']}.")  # Prints the text of the page that matches the query
