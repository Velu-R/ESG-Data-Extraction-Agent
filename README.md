# 🌍 ESG-Data-Extraction-Agent

This project is a multi-agent ESG (Environmental, Social, Governance) data extraction system built to automate the discovery, classification, and parsing of ESG reports from publicly available sources.

## 🔧 Key Features

- 🔍 **Scraper Agent**: 
  - Fetches company metadata using name.
  - Retrieves ESG peer companies based on GICS classifications.
  - Finds direct links to sustainability/ESG reports (PDF only).

- 📄 **Extractor Agent**:
  - Accepts valid `.pdf` sustainability reports.
  - Extracts structured ESG emission data using predefined schemas.
  - Merges and stores results with company ID and reporting year.

- 🧠 **Supervisor Agent**:
  - Orchestrates task flow based on user intent.
  - Delegates tasks to scraper or extractor intelligently.
  - Handles single or multi-company requests with minimal interaction.

---

## ⚙️ Tech Stack

- 🧠 [LangGraph](https://langchain-ai.github.io/langgraph/agents/multi-agent/) for orchestrating agents.
- 🌐 Tavily for real-time web search.
- 🤖 OpenAI & Gemini for LLM-based scraping and extraction.
- 🗃️ MongoDB for ESG data persistence.
- 🧪 Python 3.10+ with LangChain, Pydantic, etc.

---


# 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone git@github.com:Velu-R/ESG-Data-Extraction-Agent.git
   cd ESG-Data-Extraction-Agent

2. Install dependencies:
   ```
   pip install -r requirements.txt

3. Create a .env file in the root directory with the following environment variables:
   ```
   TAVILY_API_KEY="your-tavily-key"
   GEMINI_API_KEY="your-gemini-key"
   OPENAI_API_KEY="your-openai-key"
   MONGODB_URI="your-mongodb-uri"
   MONGODB_DB_NAME="sustainability_reports"
   LANGSMITH_API_KEY="your-langsmith-key"
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
   LANGSMITH_PROJECT="sustainability_report_extractor"

   ```

4. Run the application using LangGraph:
   ```
   langgraph dev
---

## 🔄 How It Works

1. **User** makes a request (e.g., "Extract ESG report for Tesla").
2. **Supervisor Agent** identifies intent:
   - Uses **Scraper Agent** to find the ESG report.
   - Passes the PDF to **Extractor Agent**.
3. Extracted data is:
   - Structured using ESG schemas
   - Stored in MongoDB
   - Displayed on the hosted dashboard

---

# 🛠️ Usage Scenarios

1. fetch_company_metadata
   - Input: "Can you get Zalando information?"
   - Supervisor transferred to scraper_agent → fetch_company_metadata
   - Output: Here is the information about Zalando:
   ```
      Company Name: Zalando SE
      Core: Online retail platform specializing in fashion, shoes, and beauty products
      Sector: Consumer Discretionary
      Industry Group: Consumer Discretionary Distribution & Retail
      Industry: Specialty Retail
      Sub-Industries: Apparel Retail
      Headquarters: Berlin, Germany
      Country: Germany
      Region: Europe
   ```
---
2. get_peer_companies
   - Input: "Can you get the 5 regional peers of Zalando se"
   - Supervisor transferred to scraper_agent → get_peer_companies
   - Output: Here are five companies that align closely with the criteria::
   ```
      1. H&M Group

      company_name: H&M Group
      sector: Consumer Discretionary
      industry_group: Consumer Discretionary Distribution & Retail
      industry: Specialty Retail
      sub_industries: Apparel Retail
      headquarters: Stockholm
      country: Sweden
      region: Europe
      company_official_website: https://hmgroup.com
      H&M Group is a leading global fashion retailer known for its commitment to sustainability. The company publishes an annual Sustainability Performance Report detailing its ESG initiatives. (thematictake.nridigital.com)

      2. Inditex

      company_name: Inditex
      sector: Consumer Discretionary
      industry_group: Consumer Discretionary Distribution & Retail
      industry: Specialty Retail
      sub_industries: Apparel Retail
      headquarters: Arteixo
      country: Spain
      region: Europe
      company_official_website: https://www.inditex.com
      Inditex, the parent company of brands like Zara, publishes an annual Sustainability Report outlining its ESG strategies and performance. (mdpi.com)

      3. Kering SA

      company_name: Kering SA
      sector: Consumer Discretionary
      industry_group: Consumer Discretionary Distribution & Retail
      industry: Textiles, Apparel & Luxury Goods
      sub_industries: Luxury Goods
      headquarters: Paris
      country: France
      region: Europe
      company_official_website: https://www.kering.com
      Kering SA, a luxury goods company, is recognized for its comprehensive sustainability initiatives and publishes detailed ESG reports. (spglobal.com)

      4. Moncler S.p.A.

      company_name: Moncler S.p.A.
      sector: Consumer Discretionary
      industry_group: Consumer Discretionary Distribution & Retail
      industry: Textiles, Apparel & Luxury Goods
      sub_industries: Luxury Goods
      headquarters: Milan
      country: Italy
      region: Europe
      company_official_website: https://www.monclergroup.com
      Moncler S.p.A. is noted for its sustainability efforts and is a member of the S&P Global Sustainability Yearbook. (spglobal.com)

      5. Burberry Group plc

      company_name: Burberry Group plc
      sector: Consumer Discretionary
      industry_group: Consumer Discretionary Distribution & Retail
      industry: Textiles, Apparel & Luxury Goods
      sub_industries: Luxury Goods
      headquarters: London
      country: United Kingdom
      region: Europe
      company_official_website: https://www.burberryplc.com
      Burberry Group plc is recognized for its ESG disclosures and is included in the S&P Global Sustainability Yearbook. (spglobal.com)

      While these companies may not all fall strictly within the "Apparel Retail" sub-industry, they are significant players in the European apparel and luxury goods market with substantial ESG reporting practices.
   ```
---
3. get_company_sustainability_report
   - Input: "Can you get Kering SA recent sustainability report"
   - Supervisor transferred to scraper_agent.
   - Output: Here are the recent sustainability reports for Kering SA:
   ```
   0	https://dq06ugkuram52.cloudfront.net/files/6018785/22379887.pdf
   1	https://wikirate.s3.amazonaws.com/files/5619020/21053773.pdf
   2	https://www.kering.com/api/download-file/?path=Kering_Sustainability_Progress_Report_2020_2023_ad0d18f12c.pdf
   3	https://www.kering.cn/api/download-file/?path=Dossier_de_presse_Kering_2025_Sustainability_strategy_EN_only_ffa278f1ac.pdf
   4	https://www.kering.com/api/download-file/?path=Kering_ESG_Presentation_RS_December_2023_0e40cd099e.pdf
   ```

4. extract_emission_data_as_json
   - Input: "Can you parse Kering SA recent sustainability report"
   - Supervisor transferred to extractor_agent.
   - Output: Extraction and storage completed. View your data here: https://velatest-sustainability-report-extractor.hf.space
   
---
## Tools

# Scraper Agent

- fetch_company_metadata(company_name: str)
- get_peer_companies(metadata: dict, num_country_peers: int, num_region_peers: int)
- get_company_sustainability_report(company: str, year: Optional[str] = None)

# Extractor Agent

- extract_emission_data_as_json(file_input: Union[str, bytes, BinaryIO])
- upsert_esg_report(_id: str, year: str, esg_report: Dict)

________________________________________________________________________

# 📁 ESG-Data-Extraction-Agent — Project Structure
```
📁 ESG-Data-Extraction-Agent/
|
└── src
|    └── backend                 # Core backend logic
|        ├── agents
|        │   └── agent.py        # LangGraph agent definitions
|        ├── config              # Configuration & LLM setup
|        │   ├── config.py
|        │   └── llm_factory.py
|        ├── schemas
|        │   ├── esg_schema.py
|        │   ├── gics_schema.py
|        │   ├── response_schema.py
|        │   ├── scraper_schema.py
|        │   └── state.py
|        ├── services             # External service integrations (OpenAI, Gemini, MongoDB, Tavily)
|        │   ├── gemini_service.py
|        │   ├── mongo_db_service.py
|        │   ├── openai_service.py
|        │   └── tavily_service.py
|        ├── tools                 # Tool wrappers for use by agents
|        │   └── tool.py
|        └── utils                  # Utility functions and shared logic
|            ├── common_functions.py
|            ├── logger.py
|            └── system_prompts.py      # Prompt templates for LLMs
|
├── .env             # Environment variables
├── .gitignore
├── README.md        # Project documentation
├── langgraph.json   # LangGraph runtime configuration
├── logs             # Logging output
│   └── app
│       └── sustainability_report_extractor.log
├── requirements.txt  # Python dependencies

```

## ESG Dashboard (View Extracted Data)
Once the ESG reports are processed, the extracted and structured data is automatically displayed in a hosted dashboard:

🔗 View ESG Dashboard - https://velatest-sustainability-report-extractor.hf.space/

- This application allows you to explore all extracted ESG report data in a user-friendly interface.

