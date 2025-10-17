import json
import requests
import fitz  # PyMuPDF
import datetime
from fivetran_connector_sdk.connector import Connector

# The schema of the data that the connector will output.
def schema(configuration: dict) -> dict:
    return {
        "schemas": {
            "civic_data": {
                "tables": {
                    "documents": {
                        "columns": [
                            {"name": "id", "dataType": "STRING", "primaryKey": True},
                            {"name": "source_url", "dataType": "STRING"},
                            {"name": "source_type", "dataType": "STRING"},
                            {"name": "retrieved_at", "dataType": "UTC_DATETIME"},
                            {"name": "content", "dataType": "STRING"}
                        ]
                    }
                }
            }
        }
    }

# The core of the connector. It fetches the data from the source.
def sync(configuration: dict, state: dict, schema: dict) -> dict:
    # For this example, we'll use a static URL to a sample PDF.
    # In a real implementation, this would dynamically find PDFs from a target site.
    sample_pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    print(f"Downloading PDF from {sample_pdf_url}")
    
    try:
        # Download the PDF content
        response = requests.get(sample_pdf_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        pdf_bytes = response.content

        # Extract text using PyMuPDF (fitz)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        
        doc.close()
        
        print(f"Successfully extracted {len(full_text)} characters from PDF.")

        # Yield the extracted data in the format Fivetran expects
        yield {
            "insert": {
                "documents": [
                    {
                        "id": sample_pdf_url, # Use URL as a unique ID for this example
                        "source_url": sample_pdf_url,
                        "source_type": "PDF_Minutes",
                        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "content": full_text
                    }
                ]
            }
        }

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        # Optionally, you could yield an error message to Fivetran
        yield {"log": {"level": "ERROR", "message": f"Failed to download PDF from {sample_pdf_url}: {e}"}}
    except Exception as e:
        print(f"Error processing PDF: {e}")
        yield {"log": {"level": "ERROR", "message": f"Failed to process PDF from {sample_pdf_url}: {e}"}}

# The main entry point for the Fivetran connector
if __name__ == "__main__":
    Connector(schema=schema, sync=sync).run()
