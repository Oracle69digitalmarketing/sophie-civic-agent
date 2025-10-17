import os
import google.generativeai as genai
from elasticsearch import Elasticsearch

# --- Configuration ---
# In a real app, these would come from environment variables or a config file
ES_CLOUD_ID = os.environ.get("ES_CLOUD_ID", "placeholder_cloud_id")
ES_API_KEY = os.environ.get("ES_API_KEY", "placeholder_api_key")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "placeholder_google_api_key")
INDEX_NAME = "sophie-civic-data"

# Configure the Google AI client
genai.configure(api_key=GOOGLE_API_KEY)

# --- Index Mapping ---
INDEX_MAPPING = {
    "properties": {
        "id": {"type": "keyword"},
        "source_url": {"type": "keyword"},
        "source_type": {"type": "keyword"},
        "retrieved_at": {"type": "date"},
        "content": {"type": "text"},
        "content_embedding": {
            "type": "dense_vector",
            "dims": 768, # Dimensions for the text-embedding-004 model
            "index": True,
            "similarity": "cosine"
        }
    }
}

# --- Main Functions ---

def get_es_client():
    """Initializes and returns the Elasticsearch client."""
    print("Connecting to Elasticsearch...")
    try:
        client = Elasticsearch(
            cloud_id=ES_CLOUD_ID,
            api_key=ES_API_KEY
        )
        if not client.ping():
            raise ConnectionError("Could not connect to Elasticsearch")
        print("Successfully connected to Elasticsearch.")
        return client
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None

def create_index_if_not_exists(client: Elasticsearch):
    """Creates the search index with the correct mapping if it doesn't exist."""
    print(f"Checking for index '{INDEX_NAME}'...")
    if not client.indices.exists(index=INDEX_NAME):
        print(f"Index not found. Creating index '{INDEX_NAME}' with mapping...")
        try:
            client.indices.create(
                index=INDEX_NAME,
                mappings=INDEX_MAPPING
            )
            print("Index created successfully.")
        except Exception as e:
            print(f"Error creating index: {e}")
    else:
        print("Index already exists.")

def index_document(client: Elasticsearch, doc: dict):
    """Generates an embedding for a document and indexes it into Elasticsearch."""
    try:
        print(f"Generating embedding for document id: {doc.get('id')}")
        # 1. Generate the embedding from the document's content
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=doc["content"],
            task_type="RETRIEVAL_DOCUMENT"
        )
        embedding = result['embedding']
        print("Embedding generated successfully.")

        # 2. Add the embedding to the document
        doc_to_index = {**doc, "content_embedding": embedding}

        # 3. Index the complete document into Elasticsearch
        client.index(index=INDEX_NAME, id=doc["id"], document=doc_to_index)
        print(f"Successfully indexed document id: {doc.get('id')}")

    except Exception as e:
        print(f"Error indexing document: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    es_client = get_es_client()
    if es_client:
        create_index_if_not_exists(es_client)
        
        # Example of how we would use the indexer
        sample_doc = {
            "id": "doc-123-example",
            "source_url": "http://example.com/minutes.pdf",
            "source_type": "PDF_Minutes",
            "retrieved_at": "2025-10-17T22:00:00Z",
            "content": "This is a sample document about local city planning and public parks."
        }
        index_document(es_client, sample_doc)
