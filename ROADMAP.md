# Project Roadmap: Sophie - The Civic Data Agent

## 1. Vision & Goal

**Vision:** To create an autonomous AI agent ("Sophie") that empowers journalists, city planners, non-profits, and citizens by making complex, scattered local civic data instantly accessible and understandable through natural language.

**Core Idea:** We will combine the Fivetran and Elastic challenges into a single, powerful application. Fivetran will be the ingestion engine, pulling data from unique, hard-to-reach civic sources. Elastic will be the query engine, providing an intelligent, conversational search layer. Google Cloud will be the foundation for data storage (BigQuery/GCS) and AI reasoning (Vertex AI / Gemini).

---

## 2. Development Phases

This project will be built in distinct phases, moving from data ingestion to a fully functional, AI-powered frontend.

### Phase 1: Data Ingestion (The Fivetran Challenge)

**Goal:** Create a custom Fivetran connector to bring unique civic data into Google Cloud.

1.  **Connector Scaffolding:**
    -   Initialize a new Python project for the Fivetran Connector SDK.
    -   Define the connector configuration (e.g., target city, list of news RSS feeds, government URL).
2.  **Source 1: PDF Scraping (City Council Minutes):**
    -   Implement logic to scan a target government URL for links to PDF documents.
    -   Download new or updated PDFs.
    -   Use a Python library (like `PyMuPDF`) to extract raw text content from each PDF.
3.  **Source 2: Local News Feeds:**
    -   Implement logic to parse RSS feeds from a list of local news outlets.
    -   Extract the title, publication date, and full text content from each news article.
4.  **Data Syncing:**
    -   Implement the `sync` function in the Fivetran connector to stream the extracted text data (from PDFs and news articles) to the destination.
    -   Fivetran will handle loading this data into a designated Google Cloud Storage bucket (for raw text) and/or BigQuery.

### Phase 2: Data Indexing & Search (The Elastic Challenge)

**Goal:** Make all the ingested data intelligent and searchable using Elastic.

1.  **Elasticsearch Setup:**
    -   Deploy an Elasticsearch cluster (e.g., on Elastic Cloud).
    -   Define an index mapping that is optimized for both keyword search and dense vector search (for semantic understanding).
2.  **Indexing Pipeline:**
    -   Create a process (e.g., a Cloud Function triggered by new files in GCS) that reads the new data from Fivetran's output.
    -   This process will use a Google Cloud Gen AI model to generate vector embeddings for the text content.
    -   It will then index the content and its corresponding vector embedding into Elasticsearch.

### Phase 3: The AI Agent & API

**Goal:** Build the backend logic that powers Sophie's conversational abilities.

1.  **API Scaffolding:**
    -   Create a simple backend service (e.g., using Python with FastAPI or Node.js with Express) that will serve as our API.
    -   This API will have one primary endpoint: `/chat`.
2.  **The RAG Workflow (Retrieval-Augmented Generation):**
    -   When the `/chat` endpoint receives a user query (e.g., "*What was discussed about public parks in the last city council meeting?*"), it will first convert the query into a vector embedding.
    -   It will then perform a **hybrid search** against the Elasticsearch index, using both keyword matching and vector similarity to find the most relevant documents (council minutes, news articles, etc.).
    -   The content of these top documents will be compiled into a rich context.
3.  **AI Response Generation:**
    -   This context, along with the original user query, will be sent to a **Google Cloud Gen AI model (Gemini)** with a carefully crafted prompt.
    -   The prompt will instruct the model to act as a helpful civic agent, synthesize the information from the provided context, and generate a conversational, accurate answer.
    -   The API will stream the response back to the frontend.

### Phase 4: Frontend & User Interface

**Goal:** Create a clean, intuitive, and polished user interface.

1.  **Project Setup:**
    -   Initialize a Next.js project with TypeScript.
    -   Use a modern UI component library (like Shadcn/UI) for a professional look and feel.
2.  **UI Implementation:**
    -   Build a simple, single-page application with a chat interface.
    -   The interface will have a text input for the user's question and a display area for the conversation history.
    -   The UI will handle streaming the AI's response in real-time to create a dynamic, chatbot-like experience.
3.  **Deployment:**
    -   Host the frontend on a service like Vercel or Render for easy public access.

---

## 3. Tech Stack Summary

-   **Data Connector:** Fivetran Connector SDK (Python)
-   **Data Destination:** Google BigQuery / Google Cloud Storage
-   **Search & Indexing:** Elasticsearch (Elastic Cloud)
-   **AI Reasoning:** Google Cloud Vertex AI / Gemini
-   **Backend API:** Python (FastAPI) or Node.js (Express)
-   **Frontend:** Next.js (React) with TypeScript
-   **Deployment:** Vercel (Frontend), Google Cloud Run (Backend)

---

## 4. Hackathon Submission Checklist

1.  **GitHub Repo:** Public, with `LICENSE` and `README.md`.
2.  **Live URL:** Deployed frontend on Vercel.
3.  **Demo Video (3 mins):**
    -   **Problem:** Show how hard it is to find specific civic information today.
    -   **Solution:** Demonstrate using Sophie to ask a complex question and get an instant, synthesized answer.
    -   **Impact:** Explain how this empowers communities and local journalism.
4.  **Devpost Form:** Completed with a compelling story and a link to a pitch deck.
