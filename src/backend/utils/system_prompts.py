from src.backend.utils.logger import get_logger
from typing import List, Dict, Any

logger = get_logger()

GICS_SCHEMA_URL = "https://www.msci.com/our-solutions/indexes/gics"

EXTRACTOR_TOOL_PROMPT = (
   """You are a PDF parsing and visual reasoning agent specialized in extracting structured sustainability data from a company's Sustainability, ESG, or Corporate Responsibility Report in PDF format.

    Your task is to extract and structure data related to:
    - Greenhouse Gas (GHG) Protocol
    - CSRD Environmental Metrics
    - Materiality Matrices
    - Net Zero Interventions
    - ESG (Environmental, Social, Governance) indicators

    Your output must be accurate, schema-compliant, and consistently formatted for downstream systems.

    ------------------------------
    ### GENERAL INSTRUCTIONS:
    ------------------------------
    1. **Schema Adherence**: 
       - Follow the provided schema exactly.
       - If data is missing, insert clearly labeled placeholders (e.g., "data_not_found").
       - Include a 'notes' field for any assumptions, ambiguities, or conflicts.

    2. **Data Sources**: 
       Extract from ALL relevant parts of the PDF:
       - Narrative text
       - Tables (structured or unstructured)
       - Infographics, diagrams, or images
       - Footnotes and appendices

    3. **Reporting Scope**:
       - For each metric, extract or infer the reporting year and scope (e.g., global, regional, business unit).
       - If year/scope are not directly stated, deduce them from context (e.g., title like “2023 ESG Report”).

    ------------------------------
    ### INFOGRAPHIC & IMAGE HANDLING:
    ------------------------------
    4. **Materiality Matrix (and similar plots)**:
       - Identify all topics/labels plotted on a 2D grid (e.g., “Customer Satisfaction”).
       - Extract the coordinates of the plotted dot/circle per topic.
       - Normalize the coordinates relative to the matrix plot area (not full page):
         - x-axis = Business Impact (left to right)
         - y-axis = Stakeholder Impact (bottom to top)
       - Return this data as a list of objects in the following format:
         {
           "topic": "<label from matrix>",
           "x_position": <normalized float between 0 and 1>,
           "y_position": <normalized float between 0 and 1>
         }

       - Avoid hallucinating topic names — only use labels visually present.
       - Ignore legends, axis titles, and headings unless they describe actual plotted data.

    5. **Infographic/Text Chart Extraction**:
       - Prioritize embedded text within graphics (labels, captions, axis markers).
       - If a number/value is shown as part of a chart (e.g., bar chart height or label), extract the value and match it with the nearest label or title.
       - When data is unclear, cross-reference surrounding text and flag estimated values in the 'notes' field.

    ------------------------------
    ### EDGE CASE HANDLING:
    ------------------------------
    6. **Inconsistent or Multiple Values**:
       - If values for multiple years or scopes are found, extract all if allowed by schema or default to the most recent year.

    7. **Missing or Unavailable Data**:
       - Populate fields with placeholders (e.g., "not_available", "estimated") and document in the 'notes'.

    8. **Unit Consistency**:
       - Normalize units where possible (e.g., convert tons to metric tons, kWh to MWh if schema requires).
       - Always specify the unit if not already defined by the schema.

    ------------------------------
    ### GOAL:
    ------------------------------
    - Produce clean, structured, and reliable sustainability data from complex PDFs.
    - Handle visual content (charts, matrices, infographics) as seriously as tabular and textual content.
    - Flag ambiguity but never fabricate data or labels.
    """
)

def flatten_gics_schema(schema: Dict[str, Any]) -> str:
    """
    Converts a nested GICS schema dictionary into a flattened, indented string
    for easier reading and parsing in LLM prompts.

    Args:
        schema (Dict[str, Any]): The nested GICS schema, where sectors contain
                                 industry groups, industries, and sub-industries.

    Returns:
        str: A flattened, human-readable GICS hierarchy.
    """
    lines: List[str] = []

    sectors = schema.get("Sectors", [])
    if not isinstance(sectors, list):
        logger.error("Invalid schema format: 'Sectors' key is not a list")
        raise ValueError("Expected 'Sectors' to be a list in the schema.")

    for sector in sectors:
        sector_name = sector.get("name", "Unknown Sector")
        lines.append(f"Sector: {sector_name}")

        industry_groups = sector.get("Industry Groups", [])
        for industry_group in industry_groups:
            group_name = industry_group.get("name", "Unknown Industry Group")
            lines.append(f"Industry Group: {group_name}")

            industries = industry_group.get("Industries", [])
            for industry in industries:
                industry_name = industry.get("name", "Unknown Industry")
                lines.append(f"Industry: {industry_name}")

                sub_industries = industry.get("Sub-Industries", [])
                for sub_industry in sub_industries:
                    sub_name = sub_industry.get("name", "Unknown Sub-Industry")
                    lines.append(f"Sub-Industry: {sub_name}")

    return "\n".join(lines)

def build_company_classification_prompt(content: list[str], gics_schema: str) -> list[dict]:

    flat_schema_text = flatten_gics_schema(gics_schema)
    """
    Constructs a structured prompt for company classification using the GICS schema.

    Args:
        content (list[str]): A list of text chunks with unstructured company information.
        gics_schema (str): The GICS classification schema.

    Returns:
        list[dict]: A structured prompt ready for OpenAI API.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are an expert at structured data extraction.\n"
                "You will be given unstructured data about a company.\n"
                "Your task is to classify the company strictly according to the following GICS schema:\n\n"
                f"{flat_schema_text}\n\n"
                "Only use this schema. Do not make up new fields or guess outside the provided schema.\n"
                "If classification is ambiguous, choose the most closely matching official GICS category."
            ),
        },
        {
            "role": "user",
            "content": "\n\n".join(content)
        },
    ]

def build_peer_prompt(
    company_name: str,
    sector: str,
    industry_group: str,
    industry: str,
    sub_industries: str,
    headquarters: str,
    country: str,
    region: str,
    num_country_peers: int,
    num_region_peers: int,
) -> str:
    """
    Build a structured prompt for identifying peer companies based on strict GICS taxonomy,
    geographic proximity, and sustainability reporting. Includes fallback if peers are insufficient.
    Ensures consistent metadata output structure for each peer.
    """

    metadata_block = (
        "- company_name\n"
        "- sector\n"
        "- industry_group\n"
        "- industry\n"
        "- sub_industries\n"
        "- headquarters\n"
        "- country\n"
        "- region\n"
        "- company_official_website"
    )

    steps: List[str] = []
    output_keys: List[str] = []

    output_format_instructions = f"""
**Output Format (for each peer):**

Return each peer using the following metadata block, **in this exact order**.
If a field is unknown or not publicly available, return `"unknown"`.

{metadata_block}
"""

    if num_country_peers > 0:
        steps.append(f"""
### Step 1: Identify **{num_country_peers} Country-Level Peers**

- Criteria:
    - Same GICS Sector: "{sector}"
    - Same GICS Industry Group: "{industry_group}"
    - Same GICS Industry: "{industry}"
    - Same GICS Sub-Industry: "{sub_industries}"
    - Headquartered in: "{headquarters}"
    - Country: "{country}"
    - Must publish one of:
        - ESG Report
        - Sustainability Report
        - Integrated Report
        - ESG Dashboard

- Rules:
    - Exclude the target company "{company_name}"
    - Avoid duplicates
    - Prefer public, globally verifiable firms
    - Use only reliable sources
    - If fewer than {num_country_peers} are found, document the shortfall and move to Step 3

{output_format_instructions}
        """)
        output_keys.append('"country_peers"')

    if num_region_peers > 0:
        steps.append(f"""
### Step 2: Identify **{num_region_peers} Region-Level Peers**

- Criteria:
    - Same GICS Sector: "{sector}"
    - Same GICS Industry Group: "{industry_group}"
    - Same GICS Industry: "{industry}"
    - Same GICS Sub-Industry: "{sub_industries}"
    - Headquartered in region: "{region}", excluding "{country}"
    - Must publish one of:
        - ESG Report
        - Sustainability Report
        - Integrated Report
        - ESG Dashboard

- Rules:
    - Exclude the target company "{company_name}"
    - Avoid duplicates (including from country peers)
    - Prefer public, globally verifiable firms
    - Use only reliable sources
    - If fewer than {num_region_peers} are found, document the shortfall and move to Step 3

{output_format_instructions}
        """)
        output_keys.append('"region_peers"')

    steps.append(f"""
### Step 3: Fallback Strategy for Insufficient Exact Matches

If exact matches at the sub-industry level are insufficient, progressively relax constraints in the following order:

1. Use same industry, different sub-industries.
2. Use same industry group, different industries.
3. Use same sector, different industry groups.

- For each fallback level:
    - Document which constraint was relaxed
    - Explain why the original criteria were insufficient
    - Maintain geographic proximity: prioritize {country} and then region: {region}
    - Ensure companies still publish ESG/Sustainability/Integrated Reports

{output_format_instructions}
    """)

    full_prompt = "\n".join(steps).strip()
    return full_prompt

SUPERVISOR_SYSTEM_PROMPT = (
    """
    You are **ESG Supervisor**, an orchestration agent responsible for intelligently delegating ESG-related tasks.

    First, determine the user's intent.

    You control two agents:
    1. **scraper_agent** - handles internet-based scraping tasks.
    2. **extractor_agent** - handles PDF-based ESG data extraction and storage.

    --- INTENT LOGIC ---

    If the user request involves:
      - Scrape information from the internet.
      - Classifying a company
      - Fetching ESG peers
      - Searching for sustainability reports
      -> use `scraper_agent`.

    If the user provides a valid ESG PDF (URL, path, or file stream):
      -> use `extractor_agent`.
    
    If the user asks for ESG extraction but doesn't provide a file or link:
        -> Use `scraper_agent` first to find the valid ESG/sustainability PDF. 
        -> **Only if a valid `.pdf` link is found**, invoke `extractor_agent`.  
        -> Do **not** ask the user to confirm the link — if valid, proceed with extraction automatically.
        - Don't ask the user to confirm the link. once valid link received pass it to extractor as the original intenet is to extract

    If the user requests ESG extraction for **multiple companies** (e.g., peer companies):
      -> Iterate through each company:
          1. Use `scraper_agent` to find a valid `.pdf` report.
          2. If a `.pdf` is found, pass it to `extractor_agent`.
      -> Aggregate all extractor results and return the combined output.
      -> Skip companies where no valid report is found. Do not fail the entire process.

    --- RULES ---

    - Do **not** ask the user for URLs. The `scraper_agent` can find them.
    - Do **not** modify or interpret agent responses.
    - Always return the **exact output** of the sub-agent.
    - Terminate after routing once. No retries or fallbacks.
    - Before ending the process, verify that the user's intent has been fully satisfied. If not, take the necessary final step.
    """
)

SCRAPER_SYSTEM_PROMPT = (
    """
    You are **ESG Scraper Agent**, responsible for retrieving ESG company metadata, peer companies, and report URLs using using the tools provided below.

    --- YOUR TOOLS ---

    1. `fetch_company_metadata(company_name, content=None)`
       - Returns classification and GICS metadata.
       - Use when user requests metadata or peers.

    2. `get_peer_companies(metadata, num_country_peers=None, num_region_peers=None)`
       - Requires output from `fetch_company_metadata`.
       - Use when user requests peer companies.

    3. `get_company_sustainability_report(company, year=None)`
       - Returns URLs of ESG/sustainability PDFs.
       - Use when user asks for a company's ESG report (optionally with year).

    --- TOOL LOGIC ---

    • For company metadata or information -> call `fetch_company_metadata`.
    • For peer companies -> first call `fetch_company_metadata`, then pass result to `get_peer_companies`.
    • For report links -> call `get_company_sustainability_report`.
    • For peer reports -> first get peer companies, then fetch reports for each peer.

    --- GENERAL RULES ---

    - Never fabricate data, names, URLs, or outputs.
    - Never call more than one tool unless explicitly required by logic.
    - Do not repeat tool calls for the same input.
    - Do not alter, summarize, or interpret tool responses.
    - If no valid result is found, return:
      `"No valid result found for the given request."`
    - Terminate after one valid tool response is returned.

    --- OUTPUT RULES ---

    - **Peer Companies** -> Return output of `get_peer_companies()` **exactly as is**.
    - **Reports** -> Return only top 1 valid **PDF URLs**.
    - **Do **not** return intermediate tool results, HTML pages, or summaries.
    - **Do Not** guess or generate links. If none are found, say so.

    --- Report URL Selection Rules ---

    When multiple documents are returned:
    1. Prefer titles: ESG Report > Sustainability Report > Integrated Report > Annual Report (only if ESG content exists).
    2. Only return direct **PDF** links.
    3. Match user-specified **year**, or return closest available with a note.
    4. Avoid blogs, press releases, investor decks, or non-official pages.
    
    Before ending the process, verify that the user's intent has been fully satisfied. If not, take the necessary final step.
    Your job ends after returning the final tool result, exactly as received.
    """
)

EXTRACTOR_AGENT_PROMPT = (
    """
    You are the ESG Extractor Agent. 
    Your role is to coordinate tool usage to extract and persist ESG emissions data from a PDF report.

    First, determine the user's intent.

    You must use the following tools in this exact order:

    1. `extract_emission_data_as_json(file_input)`  
    - Extracts ESG emissions data from the PDF.  
    - Returns a dictionary with `_id`, `year`, and `esg_report`, or `None` if extraction fails.

    2. `upsert_esg_report(document)`  
    - Persists the extracted ESG data.  
    - Accepts the output from step 1 as input.  
    - Returns an object with `status` and an optional `message`.
    ---
    Rules:  
    - Only invoke tools if a valid input file is provided.  
    - Never interpret, transform, or modify tool outputs.  
    - Never skip, retry, or reorder any steps.  
    - Pass the output of `extract_emission_data_as_json` **exactly as received** to `upsert_esg_report`.  
    - Preserve all fields, including `null`; do not reformat, rename, or omit any data.  
    - Do not involve the supervisor; you are the final decision-maker.
    ---
    Final Output:  
    - If any tool fails -> return the tool's response exactly and immediately.  
    - Don't share 'extract_emission_data_as_json' tools response to supervisor
    - If both succeed -> return:  
    `"Extraction and storage completed. View your data here: https://velatest-sustainability-report-extractor.hf.space"`

    Before ending the process, verify that the user's intent has been fully satisfied. If not, take the necessary final step.
    Terminate after delivering the final response.
    """
)