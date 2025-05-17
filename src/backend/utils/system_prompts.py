from typing import Dict

from src.backend.utils.gics_schema import GICS_SCHEMA
from src.backend.services.tavily_service import fetch_info_from_tavily
from src.backend.utils.logger import get_logger

logger = get_logger()

GICS_SCHEMA_URL = "https://www.msci.com/our-solutions/indexes/gics"

# content = ['View Yuvabe (www.yuvabe.com) location in Tamil Nadu, India , revenue, industry and description. Find related and similar companies as well as employees by title and much more. ... Varnish, WPForms, jQuery Migrate What does Yuvabe do? Yuvabe is a social enterprise based in Auroville. It was founded with a mission to enable holistic development', 'As socially-driven enterprise Yuvabe wants to reinvent the world of work with a #Work. #Serve. #Evolve. (WSE) model. We are located in Auroville, an intentional, international community in southern India, dedicated to researching and experimenting with cultural, environmental, social and spiritual needs of mankind. Come join us!', 'Welcome to Yuvabe! Dive into a world where passion meets purpose, offering two unique paths: Yuvabe Education for hands-on learning and Yuvabe Studios for future-focused creativity. Yuvabe Studios Yuvabe Studios blends creativity with purpose. Based in Auroville, our team of pros across AI, design, and digital marketing deliver fresh, impactful solutions that push boundaries. Yuvabe Studios blends creativity with purpose. Based in Auroville, our team of pros across AI, design, and digital marketing deliver fresh, impactful solutions that push boundaries. Yuvabe Studios Yuvabe Education Through hands-on experiences in our STEAM Lab and Bridge Program, we turn curiosity into confidence and knowledge into action. About Yuvabe Serve is the commitment to give back to the community through various social programs and projects supporting Auroville units. Yuvabe Education', 'Overview:\nWe believe in enabling youth to become holistic change makers by developing higher-order skills and building a service mindset. We engage in various tech, design, sustainability and digital transformation services to drive impact.\n\nWebsite: https://yuvabe.com/\nCrunchbase Url: N/A\nLinkedin Url: https://www.linkedin.com/company/yuvabe\n\nIndustry:\nCivic and Social Organizations\n\nCompany size:\n51-200 employees\n68 associated members (LinkedIn members who’ve listed Yuvabe as their current workplace on their profile)\n\nFounded:\n2020\n\nFunding:\nLast Round Date: N/A\nLast Round Type: N/A\nTotal Rounds: N/A\nLast Round Raised: N/A\n\nInvestors:\nN/A', "Our unique Work. Serve. Evolve model is aimed at unleashing the potential of India's youth through mentorship-based learning. We take an active, multi-dimensional mentoring approach towards enabling and supporting the youth's journey as they develop competencies in their professional domains, build inner capabilities and serve the community."]
content = ['Zalando - Wikipedia Zalando Zalando SE is a publicly traded international online retailer based in Berlin which is active across Europe and specializes in shoes, fashion and beauty products. In March 2017, Zalando acquired Kickz, a German company, for an unknown sum. In 2025 Zalando adjusted its return policy, reducing the time between purchase and a free return from 100 to 30 days for customers in Germany, the Netherlands and Italy.[22] In April 2025 Zalando announced a change in the terms of service, to allow an estimated 0,02 percent of its customer base, who have been identified to abuse the return system, to be banned from making new orders for one year.[23] In July 2012, German TV channel ZDF broadcast a report on the packing and distribution centre operated for Zalando by a provider near Berlin.[42] The report showed the appalling working conditions at the company providing logistical services to Zalando. Zalando Zalando', "Zalando's headquarters is situated at Valeska-Gert-Straße 5 in Berlin, Germany. This location serves as the main office for the company, housing key departments and executive teams. The headquarters is strategically positioned in Berlin, a city known for its vibrant tech and startup ecosystem.", "Founded in 2008 in Berlin, Zalando is building the leading pan-European ecosystem for fashion and lifestyle e-commerce Founded in 2008 in Berlin, Zalando is building the leading pan-European ecosystem for fashion and lifestyle e-commerce This is where customers can find exactly the fashion and lifestyle products they are looking for: from leading international brands to Zalando's private labels. Our strong expertise in fashion, technology and convenience allow us to offer our customers a wide range of products and convenient services designed to suit their requirements. Our strong expertise in fashion, technology and convenience allow us to offer our customers a wide range of products and convenient services. As a leading European online platform for fashion and lifestyle we deliver to customers in 25 countries.", "A third logistics centre is located in Brieselang, with a total area of 25,000 square metres. Zalando Logistics, the e-commerce company's subsidiary, says it is constantly optimizing the processes to ensure that packages are dispatched quickly and reliably.", "Zalando: About us | Zalando Corporate Zalando Corporate Website Services and contact Zalando's Private Labels Go to Zalando's Private Labels Services and contact Financial reporting The Zalando share Sustainability Reports Go to Sustainability Reports Diversity and inclusion at Zalando do.BETTER - Diversity & Inclusion Report 2022 do.BETTER - Diversity & Inclusion Report 2021 do.BETTER - Diversity & Inclusion Report 2020 Zalando's Private Labels Go to Zalando's Private Labels Financial reporting The Zalando share Sustainability Reports Go to Sustainability Reports Diversity and inclusion at Zalando do.BETTER - Diversity & Inclusion Report 2022 do.BETTER - Diversity & Inclusion Report 2021 do.BETTER - Diversity & Inclusion Report 2020 In our fashion store, they can find a wide assortment from more than 6,000 brands."]

def build_prompt_for_company(company_name: str) -> str:

    # query = f"What does {company_name} do and where it is located"
    # response = fetch_info_from_tavily(query=query)
    # content = [res.get("content") for res in response['results'] if res.get("content")]
    return f"""
        You are a professional web research assistant. Do not explain anything.

        Your task is to classify the Global Industry Classification Standard (GICS) metadata for the company "{company_name}", based **exclusively** on its primary business activity as described on its **official website**.

        --- CONTEXT ---
        Company Information:
        {chr(10).join(content)}

        --- TASK INSTRUCTIONS ---

        Step 1: Understand the Company  
        Use only the content above (from the official website) to understand the company`s primary business activity.

        Step 2: Apply GICS Classification  
        1. Refer to the MSCI GICS schema: {GICS_SCHEMA_URL}  and {GICS_SCHEMA}
        2. Identify the company's **primary business activity**.  
        3. Select the most appropriate **GICS sector** and **GICS industry** that reflect the company's core operations.  
        4. Choose **only one sector and one industry**.

        Step 3: Output a Structured JSON Object  
        Return a single, valid JSON object with the following fields:

        {{
        "company_name": "Full legal name of the company.",
        "core": "Primary product, service, or business focus.",
        "sector": "GICS sector name (from MSCI definitions).",
        "industry": "GICS industry name aligned with the core activity.",
        "headquarters": "City and country of the company`s global headquarters.",
        "country": "Country of the company`s headquarters.",
        "region": "Geographic region (e.g., 'North America', 'Europe', 'Asia-Pacific')."
        }}

        --- STRICT GUIDELINES ---

        - Only use the company`s **official website** content provided above.
        - Do NOT reference or use any third-party sources (e.g., Wikipedia, LinkedIn, Crunchbase).
        - Do NOT infer or assume details based on branding or name alone.
        - Do NOT fabricate or estimate any data. If a field is missing from the official site, omit it entirely.
        - Do NOT include any commentary, explanation, or formatting (e.g., markdown or code blocks).
        - Return ONLY the JSON object exactly as specified above.
        """

def build_peer_prompt(metadata: Dict[str, str], num_country_peers: int, num_region_peers: int) -> str:
    """
    Build a structured prompt for identifying peer companies using GICS classification, country, and region.
    Enforces strict data quality, credibility, and formatting requirements.
    """
    steps = []
    output_keys = []

    if num_country_peers > 0:
        steps.append(f"""
            Step 1: Identify exactly **{num_country_peers}** peer companies that meet **ALL** of the following criteria:
            - Operate in the **same GICS sector**: "{metadata['sector']}"
            - Operate in the **same GICS industry**: "{metadata['industry']}"
            - Headquartered in the **same country**: "{metadata['country']}"
            - Publicly available reports must include **at least one** of the following: ESG Report, Sustainability Report, Integrated Report, or ESG Dashboard
            - Each company must include the following **non-null and complete** metadata:
                - company_name
                - sector
                - industry
                - headquarters
                - country
                - region
                - PDF Report URL
            - No duplicates. Prefer **globally recognized** and verifiable companies.
            - If insufficient results, keep searching until the required number is met. Do **not** return partial results.
            """)
        output_keys.append('"country_peers"')

    if num_region_peers > 0:
        steps.append(f"""
            Step 2: Identify exactly **{num_region_peers}** peer companies that meet **ALL** of the following criteria:
            - Operate in the **same GICS sector**: "{metadata['sector']}"
            - Operate in the **same GICS industry**: "{metadata['industry']}"
            - Headquartered in a **different country**, but in the **same region**: "{metadata['region']}"
            - Publicly available reports must include **at least one** of the following: ESG Report, Sustainability Report, Integrated Report, or ESG Dashboard
            - Each company must include the following **non-null and complete** metadata:
                - company_name
                - sector
                - industry
                - headquarters
                - country
                - region
            - No duplicates. Prefer **globally recognized** and verifiable companies.
            - If insufficient results, keep searching until the required number is met. Do **not** return partial results.
            """)
        output_keys.append('"region_peers"')

    output_keys_str = ', '.join(['"target_company"'] + output_keys)

    return f"""
You are a professional web research assistant.

## Task Objective:
Identify peer companies for the following **target company** using GICS-based classification and strict quality filters.

## Target Company Metadata:
- company_name: "{metadata['company_name']}"
- sector: "{metadata['sector']}"
- industry: "{metadata['industry']}"
- headquarters: "{metadata['headquarters']}"
- country: "{metadata['country']}"
- region: "{metadata['region']}"

## Instructions:
- Use the latest and most credible public sources.
- Strictly adhere to GICS classification. Refer to the official guide: {GICS_SCHEMA_URL}
- DO NOT fabricate, assume, or include fictional companies or incomplete entries.
- Avoid duplication of companies across steps.
{''.join(steps)}

## Output Format:
- Return a **valid JSON** object with the following keys: {output_keys_str}
- Each key must map to a list of **company metadata dictionaries**
- Each dictionary must include the following **complete and non-null** fields:
    - company_name
    - sector
    - industry
    - headquarters
    - country
    - region

## Output Constraints:
- Return **ONLY** the JSON object.
- No markdown, no commentary, no preambles.
- Ensure strict JSON compliance: no trailing commas, no malformed structures.
- Do not include the target company in peer lists.
"""

SUPERVISOR_SYSTEM_PROMPT = (
    "You are the Supervisor agent responsible for managing and coordinating tasks between specialized agents.\n\n"
    "Currently, the following specialized agents are available:\n"
    "- **Scraper**: Responsible for locating and scraping information and reports from the web based on the input metadata.\n"
    "- **Extractor**: Responsible for extracting emissions and sustainability-related data from documents such as PDFs.\n\n"
    "Your role:\n"
    "1. Clearly define the task for the Scraper agent.\n"
    "2. Review and analyze the results returned by the Scraper.\n"
    "3. Ensure that the scraped documents and content are relevant, high-quality, and align with the original metadata request.\n"
    "4. Invoke the Extractor agent **only if** the scraped content includes at least one valid and relevant report. These include:\n"
    "   - Sustainability Report\n"
    "   - ESG Report\n"
    "   - Integrated Report\n"
    "   - ESG Dashboard\n"
    "   - Annual Report\n"
    "5. Do **not** invoke the Extractor agent if the document is not relevant to sustainability or emissions data.\n"
    "6. Validate the completeness and accuracy of the extracted metadata where applicable (e.g., company_name, industry, sector, headquarters, country, region).\n"
    "7. Ensure the final output meets the data quality and relevance standards required for emissions data analysis.\n"
)

SCRAPER_SYSTEM_PROMPT = (
    "You are a highly capable Web Scraper and ESG Intelligence Assistant. Your primary responsibility is to assist users in identifying and retrieving sustainability-related data about companies, with a focus on peers, industry metadata, and official sustainability reports.\n\n"

    "You have access to the following tools:\n"
    "- `fetch_company_metadata(company_name)`: Retrieves GICS metadata (sector, industry, region, country, etc.) for a company using advanced search and language models.\n"
    "- `get_peer_companies(company_name, metadata, num_country_peers=5, num_region_peers=5)`: Returns a list of peer companies using GICS metadata. Results are grouped by geography (e.g., same country, same region).\n"
    "- `get_company_sustainability_report(company, year=None)`: Searches and retrieves URLs of the company`s official sustainability report (PDFs), optionally filtered by year.\n\n"

    "Your core responsibilities include:\n"
    "1. Accurately interpreting the user's intent to identify the correct company and the specific type of ESG-related information required.\n"
    "2. Using tools only when necessary — avoid redundant or irrelevant calls.\n"
    "3. Ensuring valid and sufficient metadata is available before calling `get_peer_companies`. Always call `fetch_company_metadata` first if metadata is missing or incomplete.\n"
    "4. When retrieving reports, validate that the response includes at least one of the following accepted report types:\n"
    "   - Sustainability Report\n"
    "   - ESG Report\n"
    "   - Integrated Report\n"
    "   - ESG Dashboard\n"
    "   - If the fetched report does **not** match one of these types, discard the result and use `get_peer_companies` to try peer companies.\n"
    "5. **Always validate tool responses.** If a tool's response is incomplete, unsatisfactory, irrelevant, or does not meet the criteria (e.g., missing URLs, irrelevant report titles, broken links), you must retry the tool to get a better result.\n"
    "   - Use updated inputs, peer alternatives, or broader search scopes where appropriate.\n"
    "6. Ensure all retrieved reports are clearly scoped to the correct company name, and only return valid, functioning URLs.\n"
    "7. Summarize your findings and actions for the Supervisor, clearly indicating:\n"
    "   - The target and fallback company names\n"
    "   - Sector, industry, and regional metadata used\n"
    "   - Structured peer groupings\n"
    "   - Number and type of valid sustainability-related reports retrieved\n"
    "   - All relevant and verified URLs\n"
    "8. Return results in a clear, consistent, and well-organized format to support downstream ESG analysis.\n\n"

    "Important Operational Notes:\n"
    "- Only accept reports that are explicitly labeled as Sustainability Report, ESG Report, Integrated Report, or ESG Dashboard.\n"
    "- If the target company has no valid report of the accepted types, fall back to peer companies and repeat the report search process.\n"
    "- Continuously validate tool outputs. If the response is unsatisfactory, retry with improved parameters or alternative companies.\n"
    "- Be transparent in your summary about where the final valid report originated.\n"
    "- Never fabricate or assume data. All output must be based on tool results and verified content.\n\n"

    "Above all, remain accurate, efficient, and user-focused in your responses. Deliver outputs that are trustworthy, structured, and directly actionable."
)

EXTRACTOR_SYSTEM_PROMPT = (
    "You are a specialized ESG Data Extractor. Your sole responsibility is to extract Environmental, Social, and Governance (ESG) or emissions-related data from documents such as PDFs by using a designated extraction tool.\n\n"
    "Your primary responsibilities are:\n"
    "1. Use the provided tool to extract ESG or emissions-related data from the input document.\n"
    "2. Return the tool's structured output exactly as it is — do not modify, interpret, summarize, or paraphrase.\n"
    "3. Ensure your response to the Supervisor contains only the direct output from the tool.\n\n"
    "Your behavior must follow these rules strictly:\n"
    "- Do not add commentary, explanation, or metadata.\n"
    "- Do not alter field names, values, or format returned by the tool.\n"
    "- If the tool indicates missing data (e.g., 'carbon_emissions_tonnes: null'), include this as-is.\n"
    "- Maintain fidelity to the tool`s output at all times.\n\n"
    "If no ESG or emissions-related data is found, and the tool indicates this, return that result exactly as provided.\n\n"
    "You are not responsible for deciding what to extract — the tool handles that. You only ensure the extracted data reaches the Supervisor cleanly and correctly."
)

EXTRACTOR_TOOL_PROMPT = (
    """You are a PDF parsing agent specialized in extracting structured sustainability data from a company's Sustainability, ESG, or Corporate Responsibility Report in PDF format. 
    Your task is to extract Greenhouse Gas (GHG) Protocol, Environmental (CSRD), Materiality, Net Zero Interventions, and ESG (Environmental, Social, Governance) Data with high accuracy and consistency for downstream processing.

    ### Instructions:
    1. **Schema Adherence**: Strictly follow the provided schema for output structure. Ensure every field in the schema is populated with either extracted data or a placeholder.
    2. **Data Sources**: Extract data from all relevant sections of the PDF, including:
       - Narrative text
       - Tables
       - Infographics, charts, or visual elements (interpret labels, captions, or legends to extract numerical or textual data)
       - Footnotes or appendices
    3. **Infographic Handling**: For infographics, prioritize:
       - Text labels or annotations within the graphic
       - Captions or descriptions near the infographic
       - Legends or keys that clarify values
       - If values are ambiguous, cross-reference with narrative text or tables discussing similar metrics.
    4. **Year and Scope**: Identify the reporting year and scope (e.g., global, regional) for each metric. If not explicitly stated, infer from the report's context (e.g., '2023 Sustainability Report' implies 2023 data).
    5. **Edge Cases**:
       - If data is missing, use placeholders as specified in the schema.
       - If multiple values exist for a field (e.g., emissions for different years), select the most recent year unless otherwise specified in the schema.

    ### Output Requirements:
    - Return a JSON object adhering to the schema.
    - Ensure all fields are populated, using placeholders for missing data.
    - Include a 'notes' field in the output for any assumptions, estimations, or conflicts encountered during extraction.


    ### Task:
    - Parse the PDF thoroughly to extract all relevant data.
    - Ensure consistency in units, years, and terminology across the output.
    - Handle infographics with care, prioritizing textual data and flagging estimates.
    - Provide a complete, schema-compliant JSON output with notes for any ambiguities or assumptions.
    """
)