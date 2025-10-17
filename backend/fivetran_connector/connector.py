import json
from fivetran_connector_sdk.connector import Connector

# This function defines the schema of the data that the connector will output.
# For our Civic Data Agent, we will have a single table for all documents.
def schema(configuration: dict) -> dict:
    return {
        "schemas": {
            "civic_data": {
                "tables": {
                    "documents": {
                        "columns": [
                            {"name": "id", "dataType": "STRING", "primaryKey": True},
                            {"name": "source_url", "dataType": "STRING"},
                            {"name": "source_type", "dataType": "STRING"}, # e.g., 'PDF_Minutes', 'News_Article'
                            {"name": "retrieved_at", "dataType": "UTC_DATETIME"},
                            {"name": "content", "dataType": "STRING"}
                        ]
                    }
                }
            }
        }
    }

# This function is the core of the connector. It fetches the data from the source.
# We will implement the logic to scrape PDFs and news articles here.
def sync(configuration: dict, state: dict, schema: dict) -> dict:
    # In a real implementation, we would use the state to sync only new data.
    # For now, we will return a single piece of mock data to demonstrate.
    yield {
        "insert": {
            "documents": [
                {
                    "id": "doc-123-example",
                    "source_url": "http://example.com/minutes.pdf",
                    "source_type": "PDF_Minutes",
                    "retrieved_at": "2025-10-17T22:00:00Z",
                    "content": "This is the extracted text from a sample document."
                }
            ]
        }
    }

# The main entry point for the Fivetran connector
if __name__ == "__main__":
    Connector(schema=schema, sync=sync).run()
