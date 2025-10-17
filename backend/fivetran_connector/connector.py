import json
import requests
import fitz  # PyMuPDF
import feedparser
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
    # --- 1. PDF Data Source ---
    sample_pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    print(f"Syncing PDF from {sample_pdf_url}")
    try:
        response = requests.get(sample_pdf_url)
        response.raise_for_status()
        pdf_bytes = response.content
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = "".join(page.get_text() for page in doc)
        doc.close()
        print(f"Successfully extracted {len(full_text)} characters from PDF.")
        yield {
            "insert": {
                "documents": [
                    {
                        "id": sample_pdf_url,
                        "source_url": sample_pdf_url,
                        "source_type": "PDF_Minutes",
                        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "content": full_text
                    }
                ]
            }
        }
    except Exception as e:
        yield {"log": {"level": "ERROR", "message": f"Failed to process PDF from {sample_pdf_url}: {e}"}}

    # --- 2. RSS Feed Data Source ---
    # For this example, we'll use a static URL to a sample RSS feed.
    sample_rss_url = "http://feeds.bbci.co.uk/news/rss.xml"
    print(f"Syncing RSS from {sample_rss_url}")
    try:
        feed = feedparser.parse(sample_rss_url)
        print(f"Found {len(feed.entries)} articles in RSS feed.")
        
        articles = []
        for entry in feed.entries:
            articles.append({
                "id": entry.id,
                "source_url": entry.link,
                "source_type": "News_Article",
                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "content": f"{entry.title}\n\n{entry.summary}"
            })
        
        # Yield all articles from this source in a single batch
        if articles:
            yield {
                "insert": {
                    "documents": articles
                }
            }

    except Exception as e:
        yield {"log": {"level": "ERROR", "message": f"Failed to process RSS feed from {sample_rss_url}: {e}"}}

# The main entry point for the Fivetran connector
if __name__ == "__main__":
    Connector(schema=schema, sync=sync).run()
