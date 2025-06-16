The workflow is composed of two main subgraphs (agents):

1. **Scraper Agent**: Gathers information about the company, including sustainability-related data and public report URLs.
2. **Extractor Agent**: Extracts structured ESG data from sustainability report PDFs using schema-driven LLMs.

These subgraphs are orchestrated by a **Supervisor Agent**, which manages the overall workflow and coordinates state transitions between agents.

---

## Agent & Subgraph Design

### 1. Scraper  Subgraph (`nodes/scraper.py`)

**Purpose:**
Gathers sustainability-related company data by leveraging a combination of Tavily search results and OpenAI classification. This includes general company metadata, peer company identification, and discovery of ESG report URLs.

**Tools:**
- `fetch_company_metadata`: Uses Tavily to gather descriptive company info and classifies it using the GICS schema via OpenAI.
- `get_peer_companies`: Extracts peer companies by analyzing GICS classification and generating a structured query for OpenAI.
- `get_company_sustainability_report`: Searches for ESG-related PDF links based on company name and optional year.

**Key Features:**

- LLM-assisted classification: Company data is classified using OpenAI against a structured schema (GICS).
- Intelligent peer discovery: Generates realistic industry-specific peers based on structured metadata.
- Smart ESG scraping: Targets PDF-based ESG reports with year-aware, search-optimized queries using Tavily.

---

### 2.Extractor Subgraph (`nodes/extractor.py`)

**Purpose:**
Extracts structured emission-related data from sustainability reports (PDFs) and stores the parsed output into a database or persistent storage for further analysis.

**Tools:**

- `extract_emission_data_as_json`: Uses an LLM to parse sustainability report content and extract emission-related information in a structured  JSON format.

- `upsert_esg_report`: Saves or updates the extracted ESG data into a backend or vector database, associating it with the source document and company metadata.

**Key Features:**

- Structured extraction: Emission data is parsed using OpenAI models based on a defined emission schema.
- Automatic persistence: Parsed output is seamlessly upserted into a long-term storage layer.
---

## Main Graph Wiring

The **supervisor** orchestrates the full workflow by chaining the subgraphs:


## How to Run

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
    ```
    TAVILY_API_KEY="Your Key"
    GEMINI_API_KEY="Your Key"
    OPENAI_API_KEY="Your Key"
    MONGODB_URI=mongodb+srv://velatest03:4TfA1ob6jfe58OOR@sustainabilityreports.xbpl7kj.mongodb.net/
    MONGODB_DB_NAME=sustainability_reports
    ```

3. **Run:**
   ```
   langgraph dev
   ```

---
