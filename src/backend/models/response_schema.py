from pydantic import BaseModel, Field
from typing import Optional

GEMINI_GHG_PARAMETERS = {
    "type": "object",
    "properties": {
        "Company Name": {
        "type": "string",
        "description": "Name of the company."
        },
        "Greenhouse Gas (GHG) Protocol Parameters": {
        "type": "object",
        "properties": {
            "Total GHG Emissions": { "type": "integer", "nullable": True, "description": "Total greenhouse gases emitted by the organization. Units: Metric Tons CO₂e." },
            "Scope 1 Emissions": { "type": "integer", "nullable": True, "description": "Direct GHG emissions from owned or controlled sources. Units: Metric Tons CO₂e." },
            "Scope 2 Emissions": { "type": "integer", "nullable": True, "description": "Indirect GHG emissions from the consumption of purchased electricity, steam, heating, and cooling. Units: Metric Tons CO₂e." },
            "Scope 3 Emissions": { "type": "integer", "nullable": True, "description": "Other indirect emissions occurring in the value chain, including both upstream and downstream emissions. Units: Metric Tons CO₂e." },
            "CO₂ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of carbon dioxide. Units: Metric Tons CO₂." },
            "CH₄ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of methane. Units: Metric Tons CH₄." },
            "N₂O Emissions": { "type": "integer", "nullable": True, "description": "Emissions of nitrous oxide. Units: Metric Tons N₂O." },
            "HFC Emissions": { "type": "integer", "nullable": True, "description": "Emissions of hydrofluorocarbons. Units: Metric Tons HFCs" },
            "PFC Emissions": { "type": "integer", "nullable": True, "description": "Emissions of perfluorocarbons. Units: Metric Tons PFCs" },
            "SF₆ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of sulfur hexafluoride. Units: Metric Tons SF₆." },
            "NF₃ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of nitrogen trifluoride. Units: Metric Tons NF₃." },
            "Biogenic CO₂ Emissions": { "type": "integer", "nullable": True, "description": "CO₂ emissions from biological sources. Units: Metric Tons CO₂." },
            "Emissions Intensity per Revenue": { "type": "number", "nullable": True, "description": "GHG emissions per unit of revenue. Units: Metric Tons CO₂e / Revenue." },
            "Emissions Intensity per Employee": { "type": "number", "nullable": True, "description": "GHG emissions per employee. Units: Metric Tons CO₂e / Employee." },
            "Base Year Emissions": { "type": "integer", "nullable": True, "description": "GHG emissions in the base year for comparison. Units: Metric Tons CO₂e." },
            "Emissions Reduction Target": { "type": "number", "nullable": True, "description": "Targeted percentage reduction in GHG emissions. Units: Percentage (%)." },
            "Emissions Reduction Achieved": { "type": "number", "nullable": True, "description": "Actual percentage reduction in GHG emissions achieved. Units: Percentage (%)." },
            "Energy Consumption": { "type": "number", "nullable": True, "description": "Total energy consumed by the organization. Units: MWh or GJ." },
            "Renewable Energy Consumption": { "type": "number", "nullable": True, "description": "Amount of energy consumed from renewable sources. Units: MWh or GJ." },
            "Non-Renewable Energy Consumption": { "type": "number", "nullable": True, "description": "Amount of energy consumed from non-renewable sources. Units: MWh or GJ." },
            "Energy Intensity per Revenue": { "type": "number", "nullable": True, "description": "Energy consumption per unit of revenue. Units: MWh or GJ / Revenue." },
            "Energy Intensity per Employee": { "type": "number", "nullable": True, "description": "Energy consumption per employee. Units: MWh or GJ / Employee." },
            "Fuel Consumption": { "type": "number", "nullable": True, "description": "Total fuel consumed by the organization. Units: Liters or GJ." },
            "Electricity Consumption": { "type": "number", "nullable": True, "description": "Total electricity consumed. Units: MWh." },
            "Heat Consumption": { "type": "number", "nullable": True, "description": "Total heat energy consumed. Units: GJ." },
            "Steam Consumption": { "type": "number", "nullable": True, "description": "Total steam energy consumed. Units: GJ." },
            "Cooling Consumption": { "type": "number", "nullable": True, "description": "Total energy consumed for cooling. Units: GJ." },
            "Purchased Goods and Services Emissions": { "type": "integer", "nullable": True, "description": "Emissions from purchased goods and services. Units: Metric Tons CO₂e." },
            "Capital Goods Emissions": { "type": "integer", "nullable": True, "description": "Emissions from the production of capital goods. Units: Metric Tons CO₂e." },
            "Fuel- and Energy-Related Activities Emissions": { "type": "integer", "nullable": True, "description": "Emissions related to fuel and energy production not included in Scope 1 or 2. Units: Metric Tons CO₂e." },
            "Upstream Transportation and Distribution Emissions": { "type": "integer", "nullable": True, "description": "Emissions from transportation and distribution in the supply chain. Units: Metric Tons CO₂e." },
            "Waste Generated in Operations Emissions": { "type": "integer", "nullable": True, "description": "Emissions from waste generated during operations. Units: Metric Tons CO₂e." },
            "Business Travel Emissions": { "type": "integer", "nullable": True, "description": "Emissions from employee business travel. Units: Metric Tons CO₂e." },
            "Employee Commuting Emissions": { "type": "integer", "nullable": True, "description": "Emissions from employees commuting to and from work. Units: Metric Tons CO₂e." },
            "Upstream Leased Assets Emissions": { "type": "integer", "nullable": True, "description": "Emissions from leased assets upstream in the value chain. Units: Metric Tons CO₂e." },
            "Downstream Transportation and Distribution Emissions": { "type": "integer", "nullable": True, "description": "Emissions from transportation and distribution of sold products. Units: Metric Tons CO₂e." },
            "Processing of Sold Products Emissions": { "type": "integer", "nullable": True, "description": "Emissions from processing intermediate products sold by the organization. Units: Metric Tons CO₂e." },
            "Use of Sold Products Emissions": { "type": "integer", "nullable": True, "description": "Emissions from the use of sold products by consumers. Units: Metric Tons CO₂e." },
            "End-of-Life Treatment of Sold Products Emissions": { "type": "integer", "nullable": True, "description": "Emissions from the disposal of sold products at end of life. Units: Metric Tons CO₂e." },
            "Downstream Leased Assets Emissions": { "type": "integer", "nullable": True, "description": "Emissions from leased assets downstream in the value chain. Units: Metric Tons CO₂e." },
            "Franchises Emissions": { "type": "integer", "nullable": True, "description": "Emissions from franchise operations. Units: Metric Tons CO₂e." },
            "Investments Emissions": { "type": "integer", "nullable": True, "description": "Emissions from investments. Units: Metric Tons CO₂e." },
            "Carbon Offsets Purchased": { "type": "integer", "nullable": True, "description": "Amount of carbon offsets purchased. Units: Metric Tons CO₂e." },
            "Net GHG Emissions": { "type": "integer", "nullable": True, "description": "GHG emissions after accounting for offsets. Units: Metric Tons CO₂e." },
            "Carbon Sequestration": { "type": "integer", "nullable": True, "description": "Amount of CO₂ sequestered or captured. Units: Metric Tons CO₂e." }
        },
        "propertyOrdering": [
            "Total GHG Emissions", "Scope 1 Emissions", "Scope 2 Emissions", "Scope 3 Emissions", "CO₂ Emissions",
            "CH₄ Emissions", "N₂O Emissions", "HFC Emissions", "PFC Emissions", "SF₆ Emissions", "NF₃ Emissions",
            "Biogenic CO₂ Emissions", "Emissions Intensity per Revenue", "Emissions Intensity per Employee",
            "Base Year Emissions", "Emissions Reduction Target", "Emissions Reduction Achieved", "Energy Consumption",
            "Renewable Energy Consumption", "Non-Renewable Energy Consumption", "Energy Intensity per Revenue",
            "Energy Intensity per Employee", "Fuel Consumption", "Electricity Consumption", "Heat Consumption",
            "Steam Consumption", "Cooling Consumption", "Purchased Goods and Services Emissions", "Capital Goods Emissions",
            "Fuel- and Energy-Related Activities Emissions", "Upstream Transportation and Distribution Emissions",
            "Waste Generated in Operations Emissions", "Business Travel Emissions", "Employee Commuting Emissions",
            "Upstream Leased Assets Emissions", "Downstream Transportation and Distribution Emissions",
            "Processing of Sold Products Emissions", "Use of Sold Products Emissions", "End-of-Life Treatment of Sold Products Emissions",
            "Downstream Leased Assets Emissions", "Franchises Emissions", "Investments Emissions", "Carbon Offsets Purchased", "Net GHG Emissions",
            "Carbon Sequestration"
        ]
        },
    },
    "propertyOrdering": ["Company Name", "Greenhouse Gas (GHG) Protocol Parameters",]
}

GEMINI_ENVIRONMENTAL_PARAMETERS_CSRD = {
    "type": "object",
    "properties": {
        "Company Name": {
            "type": "string",
            "description": "Name of the company."
        },
        "Environmental Parameters (CSRD)": {
            "type": "object",
            "properties": {
                "Environmental Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies related to environmental management and sustainability."
                },
                "Environmental Management System (EMS)": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Existence of an environmental management system."
                },
                "Environmental Certifications": {
                    "type": "string",
                    "nullable": True,
                    "description": "Certifications related to environmental standards."
                }
            },
            "propertyOrdering": [
                "Environmental Policies",
                "Environmental Management System (EMS)",
                "Environmental Certifications"
            ]
        }
    },
    "propertyOrdering": ["Company Name", "Environmental Parameters (CSRD)"]
}

GEMINI_ENVIRONMENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "Company Name": {
        "type": "string",
        "description": "Name of the company."
        },
        "Environmental Parameters": {
            "type": "object",
            "properties": {
                "Air Emissions": {
                    "type": "integer", "nullable": True, "description": "Total emissions of pollutants into the air. Units: Metric Tons."
                },
                "Water Withdrawal": {
                    "type": "integer", "nullable": True, "description": "Total volume of water extracted from all sources. Units: Cubic Meters."
                },
                "Water Discharge": {
                    "type": "integer", "nullable": True, "description": "Total volume of water discharged back into the environment. Units: Cubic Meters."
                },
                "Waste Generation": {
                    "type": "integer", "nullable": True, "description": "Total amount of waste generated by the organization. Units: Metric Tons."
                },
                "Hazardous Waste": {
                    "type": "integer", "nullable": True, "description": "Amount of waste classified as hazardous. Units: Metric Tons."
                },
                "Non-Hazardous Waste": {
                    "type": "integer", "nullable": True, "description": "Amount of waste not classified as hazardous. Units: Metric Tons."
                },
                "Recycled Waste": {
                    "type": "integer", "nullable": True, "description": "Amount of waste diverted from landfills through recycling. Units: Metric Tons."
                },
                "Energy Consumption": {
                    "type": "number", "nullable": True, "description": "Total energy consumed by the organization. Units: MWh or GJ."
                },
                "Renewable Energy Consumption": {
                    "type": "number", "nullable": True, "description": "Amount of energy consumed from renewable sources. Units: MWh or GJ."
                },
                "Non-Renewable Energy Consumption": {
                    "type": "number", "nullable": True, "description": "Amount of energy consumed from non-renewable sources. Units: MWh or GJ."
                },
                "Energy Intensity": {
                    "type": "number", "nullable": True, "description": "Energy consumption per unit of output or revenue. Units: MWh or GJ per unit."
                },
                "Water Intensity": {
                    "type": "number", "nullable": True, "description": "Water consumption per unit of output or revenue. Units: Cubic Meters per unit."
                },
                "Biodiversity Impact": {
                    "type": "string", "nullable": True, "description": "Description of the organization's impact on biodiversity."
                },
                "Environmental Fines": {
                    "type": "number", "nullable": True, "description": "Total monetary value of fines for environmental violations. Units: Currency."
                },
                "Environmental Investments": {
                    "type": "number", "nullable": True, "description": "Total investments in environmental protection measures. Units: Currency."
                },
                "Environmental Certifications": {
                    "type": "string", "nullable": True, "description": "Certifications related to environmental standards (e.g., ISO 14001)."
                },
                "Environmental Management System (EMS)": {
                    "type": "boolean", "nullable": True, "description": "Existence of an environmental management system."
                },
                "Climate Change Risks": {
                    "type": "string", "nullable": True, "description": "Description of risks related to climate change affecting the organization."
                },
                "Climate Change Opportunities": {
                    "type": "string", "nullable": True, "description": "Description of opportunities related to climate change for the organization."
                },
                "Emissions Reduction Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at reducing GHG emissions."
                },
                "Renewable Energy Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives to increase the use of renewable energy sources."
                },
                "Water Conservation Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at reducing water consumption."
                },
                "Waste Reduction Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at reducing waste generation."
                },
                "Circular Economy Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives promoting the reuse and recycling of materials."
                },
                "Sustainable Sourcing Policies": {
                    "type": "string", "nullable": True, "description": "Policies ensuring procurement of sustainable materials."
                },
                "Supplier Environmental Assessment": {
                    "type": "string", "nullable": True, "description": "Assessment of suppliers' environmental practices."
                },
                "Product Environmental Footprint": {
                    "type": "string", "nullable": True, "description": "Environmental impact assessment of products."
                },
                "Packaging Environmental Impact": {
                    "type": "string", "nullable": True, "description": "Environmental impact of product packaging."
                },
                "Transportation Environmental Impact": {
                    "type": "string", "nullable": True, "description": "Environmental impact of transportation and logistics."
                },
                "Environmental Training Programs": {
                    "type": "string", "nullable": True, "description": "Training programs focused on environmental awareness."
                },
                "Environmental Grievance Mechanisms": {
                    "type": "string", "nullable": True, "description": "Mechanisms for stakeholders to report environmental concerns."
                },
                "Environmental Compliance": {
                    "type": "boolean", "nullable": True, "description": "Adherence to environmental laws and regulations."
                },
                "Environmental Goals and Targets": {
                    "type": "string", "nullable": True, "description": "Specific environmental performance goals set by the organization."
                },
                "Environmental Performance Monitoring": {
                    "type": "string", "nullable": True, "description": "Systems in place to monitor environmental performance."
                },
                "Environmental Reporting": {
                    "type": "string", "nullable": True, "description": "Public reporting of environmental performance and initiatives."
                },
                "Environmental Stakeholder Engagement": {
                    "type": "string", "nullable": True, "description": "Engagement with stakeholders on environmental matters."
                },
                "Environmental Risk Assessment": {
                    "type": "string", "nullable": True, "description": "Assessment of environmental risks associated with operations."
                },
                "Environmental Impact Assessments": {
                    "type": "string", "nullable": True, "description": "Studies conducted to assess environmental impacts of projects."
                },
                "Environmental Restoration Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at restoring damaged ecosystems."
                },
                "Environmental Advocacy and Partnerships": {
                    "type": "string", "nullable": True, "description": "Participation in environmental advocacy and partnerships."
                },
                "Environmental Awards and Recognitions": {
                    "type": "string", "nullable": True, "description": "Awards received for environmental performance."
                }
            },
            "propertyOrdering": ["Air Emissions", "Water Withdrawal", "Water Discharge", "Waste Generation",
            "Hazardous Waste",
            "Non-Hazardous Waste",
            "Recycled Waste",
            "Energy Consumption",
            "Renewable Energy Consumption",
            "Non-Renewable Energy Consumption",
            "Energy Intensity",
            "Water Intensity",
            "Biodiversity Impact",
            "Environmental Fines",
            "Environmental Investments",
            "Environmental Certifications",
            "Environmental Management System (EMS)",
            "Climate Change Risks",
            "Climate Change Opportunities",
            "Emissions Reduction Initiatives",
            "Renewable Energy Initiatives",
            "Water Conservation Initiatives",
            "Waste Reduction Initiatives",
            "Circular Economy Initiatives",
            "Sustainable Sourcing Policies",
            "Supplier Environmental Assessment",
            "Product Environmental Footprint",
            "Packaging Environmental Impact",
            "Transportation Environmental Impact",
            "Environmental Training Programs",
            "Environmental Grievance Mechanisms",
            "Environmental Compliance",
            "Environmental Goals and Targets",
            "Environmental Performance Monitoring",
            "Environmental Reporting",
            "Environmental Stakeholder Engagement",
            "Environmental Risk Assessment",
            "Environmental Impact Assessments",
            "Environmental Restoration Initiatives",
            "Environmental Advocacy and Partnerships",
            "Environmental Awards and Recognitions" ]
        },
    },
    "propertyOrdering": ["Company Name", "Environmental Parameters"]
}

GEMINI_SOCIAL_PARAMETERS = {
    "type": "object",
    "properties": {
        "Company Name": {
        "type": "string",
        "description": "Name of the company."
        },
        "Social Parameters": {
            "type": "object",
            "properties": {
                "Total Workforce": {
                    "type": "integer", "nullable": True, "description": "Total number of employees in the organization. Units: Number of Employees."
                },
                "Employee Turnover Rate": {
                    "type": "number", "nullable": True, "description": "Percentage of employees leaving the organization over a period. Units: Percentage (%)."
                },
                "Gender Diversity": {
                    "type": "number", "nullable": True, "description": "Proportion of male and female employees. Units: Percentage (%)."
                },
                "Employee Training Hours": {
                    "type": "number", "nullable": True, "description": "Total hours spent on employee training. Units: Hours."
                },
                "Health and Safety Incidents": {
                    "type": "integer", "nullable": True, "description": "Total number of health and safety incidents reported. Units: Number of Incidents."
                },
                "Lost Time Injury Rate (LTIR)": {
                    "type": "number", "nullable": True, "description": "Number of injuries resulting in lost work time per million hours worked. Units: Number of Injuries per Million Hours Worked."
                },
                "Employee Engagement Score": {
                    "type": "number", "nullable": True, "description": "Measure of employee engagement and satisfaction. Units: Score."
                },
                "Collective Bargaining Coverage": {
                    "type": "number", "nullable": True, "description": "Percentage of employees covered by collective bargaining agreements. Units: Percentage (%)."
                },
                "Human Rights Policies": {
                    "type": "string", "nullable": True, "description": "Policies related to the protection of human rights within the organization."
                },
                "Supplier Social Assessment": {
                    "type": "string", "nullable": True, "description": "Assessment of suppliers' social practices."
                },
                "Community Engagement Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at engaging and supporting local communities."
                },
                "Customer Satisfaction Score": {
                    "type": "number", "nullable": True, "description": "Measure of customer satisfaction with the organization's products or services. Units: Score."
                },
                "Product Safety Incidents": {
                    "type": "integer", "nullable": True, "description": "Total number of product safety incidents reported. Units: Number of Incidents."
                },
                "Data Privacy Breaches": {
                    "type": "integer", "nullable": True, "description": "Total number of data privacy breaches reported. Units: Number of Breaches."
                },
                "Non-Discrimination Policies": {
                    "type": "string", "nullable": True, "description": "Policies ensuring non-discrimination."
                }
            },
            "propertyOrdering": [
                "Total Workforce",
                "Employee Turnover Rate",
                "Gender Diversity",
                "Employee Training Hours",
                "Health and Safety Incidents",
                "Lost Time Injury Rate (LTIR)",
                "Employee Engagement Score",
                "Collective Bargaining Coverage",
                "Human Rights Policies",
                "Supplier Social Assessment",
                "Community Engagement Initiatives",
                "Customer Satisfaction Score",
                "Product Safety Incidents",
                "Data Privacy Breaches",
                "Non-Discrimination Policies"
            ]
        }
    
    },
    "propertyOrdering": ["Company Name", "Social Parameters",]
}

GEMINI_GOVERNANCE_PARAMETERS = {
    "type": "object",
    "properties": {
        "Company Name": {
            "type": "string",
            "description": "Name of the company."
        },
        "Governance Parameters": {
            "type": "object",
            "properties": {
                "Board Composition": {
                    "type": "string",
                    "nullable": True,
                    "description": "Details about the structure of the board, including the number of executive and non-executive directors."
                },
                "Board Diversity": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of board members by gender, ethnicity, or other diversity metrics. Units: Percentage (%)."
                },
                "Independent Directors": {
                    "type": "number",
                    "nullable": True,
                    "description": "Number or percentage of directors who are independent of the company's management. Units: Number or Percentage (%)."
                },
                "Board Committees": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on existing board committees such as audit, remuneration, and nomination committees."
                },
                "Executive Compensation": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total compensation awarded to executives, including salary, bonuses, and stock options. Units: Currency."
                },
                "CEO Pay Ratio": {
                    "type": "number",
                    "nullable": True,
                    "description": "Ratio of CEO compensation to the median employee compensation. Units: Ratio."
                },
                "Succession Planning": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies and procedures in place for executive succession planning."
                },
                "Shareholder Rights": {
                    "type": "string",
                    "nullable": True,
                    "description": "Description of shareholder voting rights and any restrictions."
                },
                "Ownership Structure": {
                    "type": "string",
                    "nullable": True,
                    "description": "Breakdown of ownership by major shareholders, institutional investors, etc."
                },
                "Anti-Corruption Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies and measures implemented to prevent corruption and bribery within the organization."
                },
                "Whistleblower Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems in place for employees and stakeholders to report unethical behavior anonymously."
                },
                "Risk Management Framework": {
                    "type": "string",
                    "nullable": True,
                    "description": "Description of the organization's approach to identifying and managing risks."
                },
                "Compliance with Laws and Regulations": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on the company's compliance with relevant laws and regulations."
                },
                "Political Contributions": {
                    "type": "number",
                    "nullable": True,
                    "description": "Amount of money contributed to political parties, candidates, or lobbying efforts. Units: Currency."
                },
                "Data Privacy Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies related to the protection of personal and sensitive data."
                },
                "Cybersecurity Measures": {
                    "type": "string",
                    "nullable": True,
                    "description": "Description of measures taken to protect the organization's information systems."
                },
                "Business Ethics Training": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total hours of training provided to employees on business ethics. Units: Number of Hours."
                },
                "Conflicts of Interest Policy": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies addressing how conflicts of interest are managed within the organization."
                },
                "Code of Conduct": {
                    "type": "string",
                    "nullable": True,
                    "description": "Document outlining the principles and standards of behavior expected from employees and management."
                },
                "Transparency in Financial Reporting": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on the organization's practices for transparent and accurate financial reporting."
                },
                "Tax Transparency": {
                    "type": "string",
                    "nullable": True,
                    "description": "Disclosure of the company's tax strategy and payments in different jurisdictions."
                },
                "Supply Chain Governance": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies and practices governing the ethical behavior of suppliers and contractors."
                },
                "Intellectual Property Rights": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies related to the protection and management of intellectual property."
                },
                "Environmental Governance": {
                    "type": "string",
                    "nullable": True,
                    "description": "Governance structures in place to oversee environmental sustainability initiatives."
                },
                "Social Governance": {
                    "type": "string",
                    "nullable": True,
                    "description": "Governance structures in place to oversee social responsibility initiatives."
                },
                "Stakeholder Engagement Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies outlining how the organization engages with stakeholders."
                },
                "Legal Proceedings": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on any significant legal proceedings involving the company."
                },
                "Internal Controls": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems and procedures in place to ensure the integrity of financial and accounting information."
                },
                "Auditor Independence": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring the independence of external auditors from the company's management."
                },
                "ESG Reporting": {
                    "type": "string",
                    "nullable": True,
                    "description": "Practices related to the disclosure of environmental, social, and governance performance."
                },
                "Board Evaluation Processes": {
                    "type": "string",
                    "nullable": True,
                    "description": "Procedures for assessing the performance and effectiveness of the board of directors."
                },
                "Remuneration Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies governing the remuneration of executives and other employees."
                },
                "Ethical Sourcing Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring that sourcing of materials and services is conducted ethically."
                },
                "Human Rights Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies outlining the company's commitment to upholding human rights within its operations and supply chain."
                },
                "Diversity and Inclusion Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies promoting diversity and inclusion within the workplace."
                },
                "Incident Reporting Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems for reporting and addressing incidents of non-compliance or unethical behavior."
                },
                "ESG Integration in Strategy": {
                    "type": "string",
                    "nullable": True,
                    "description": "How environmental, social, and governance factors are integrated into the company's overall strategy."
                },
                "Regulatory Compliance Training": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total hours of training provided to employees on regulatory compliance. Units: Number of Hours."
                },
                "Investor Relations Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies governing communication and engagement with investors and shareholders."
                },
                "Crisis Management Plans": {
                    "type": "string",
                    "nullable": True,
                    "description": "Preparedness plans for managing crises that could impact the organization's operations or reputation."
                },
                "Product Responsibility Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring that products and services meet safety and quality standards."
                },
                "Legal Compliance Incidents": {
                    "type": "number",
                    "nullable": True,
                    "description": "Number of incidents where the company was found in violation of laws or regulations. Units: Number of Incidents."
                },
                "Ethical Marketing Practices": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring that marketing and advertising practices are conducted ethically."
                },
                "ESG Performance Metrics": {
                    "type": "string",
                    "nullable": True,
                    "description": "Key performance indicators used to measure ESG performance."
                },
                "Board Meeting Attendance": {
                    "type": "number",
                    "nullable": True,
                    "description": "Percentage of board meetings attended by each director. Units: Percentage (%)."
                },
                "Shareholder Engagement Activities": {
                    "type": "string",
                    "nullable": True,
                    "description": "Activities undertaken to engage and communicate with shareholders."
                },
                "Legal Fines and Penalties": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total amount paid in fines and penalties for legal or regulatory infractions. Units: Currency."
                },
                "ESG Oversight Responsibility": {
                    "type": "string",
                    "nullable": True,
                    "description": "Identification of board members or committees responsible for ESG oversight."
                }
            },
            "propertyOrdering": [
                "Board Composition",
                "Board Diversity",
                "Independent Directors",
                "Board Committees",
                "Executive Compensation",
                "CEO Pay Ratio",
                "Succession Planning",
                "Shareholder Rights",
                "Ownership Structure",
                "Anti-Corruption Policies",
                "Whistleblower Mechanisms",
                "Risk Management Framework",
                "Compliance with Laws and Regulations",
                "Political Contributions",
                "Data Privacy Policies",
                "Cybersecurity Measures",
                "Business Ethics Training",
                "Conflicts of Interest Policy",
                "Code of Conduct",
                "Transparency in Financial Reporting",
                "Tax Transparency",
                "Supply Chain Governance",
                "Intellectual Property Rights",
                "Environmental Governance",
                "Social Governance",
                "Stakeholder Engagement Policies",
                "Legal Proceedings",
                "Internal Controls",
                "Auditor Independence",
                "ESG Reporting",
                "Board Evaluation Processes",
                "Remuneration Policies",
                "Ethical Sourcing Policies",
                "Human Rights Policies",
                "Diversity and Inclusion Policies",
                "Incident Reporting Mechanisms",
                "ESG Integration in Strategy",
                "Regulatory Compliance Training",
                "Investor Relations Policies",
                "Crisis Management Plans",
                "Product Responsibility Policies",
                "Legal Compliance Incidents",
                "Ethical Marketing Practices",
                "ESG Performance Metrics",
                "Board Meeting Attendance",
                "Shareholder Engagement Activities",
                "Legal Fines and Penalties",
                "ESG Oversight Responsibility"
            ]
        }
    },
    "propertyOrdering": ["Company Name", "Governance Parameters"]
}

GEMINI_MATERIALITY_PARAMETERS = {
    "type": "object",
    "properties": {
        "Company Name": {
            "type": "string",
            "description": "Name of the company."
        },
        "Materiality Parameters": {
            "type": "object",
            "properties": {
                "Stakeholder Engagement Level": {
                    "type": "number",
                    "nullable": True,
                    "description": "Degree to which stakeholders are involved in organizational activities or decisions. Units: Number or Percentage (%)."
                },
                "Stakeholder Feedback Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems in place for stakeholders to provide feedback to the organization."
                },
                "Identification of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Process of determining the most significant environmental, social, and governance issues relevant to the organization."
                },
                "Prioritization of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Ranking of identified material issues based on their significance to stakeholders and the organization."
                },
                "Double Materiality Assessment": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Evaluation considering both the organization's impact on sustainability matters and the impact of sustainability matters on the organization."
                },
                "Materiality Matrix Development": {
                    "type": "string",
                    "nullable": True,
                    "description": "Creation of a visual representation (matrix) plotting material issues based on their importance to stakeholders and the organization."
                },
                "Regular Review of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Frequency and process for updating the assessment of material issues."
                },
                "Integration of Material Issues into Strategy": {
                    "type": "string",
                    "nullable": True,
                    "description": "How identified material issues are incorporated into the organization's strategic planning."
                },
                "Disclosure of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Public reporting on identified material issues and how they are managed."
                },
                "Impact Assessment of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Analysis of the potential or actual impact of material issues on the organization and its stakeholders."
                }
            },
            "propertyOrdering": [
                "Stakeholder Engagement Level",
                "Stakeholder Feedback Mechanisms",
                "Identification of Material Issues",
                "Prioritization of Material Issues",
                "Double Materiality Assessment",
                "Materiality Matrix Development",
                "Regular Review of Material Issues",
                "Integration of Material Issues into Strategy",
                "Disclosure of Material Issues",
                "Impact Assessment of Material Issues"
            ]
        }
    
    },
    "propertyOrdering": ["Company Name", "Materiality Parameters"]
}

GEMINI_NET_ZERO_INTERVENTION_PARAMETERS = {
    "type": "object",
    "properties": {
        "Company Name": {
            "type": "string",
            "description": "Name of the company."
        },
        "Net Zero Intervention Parameters": {
            "type": "object",
            "properties": {
                "Renewable Energy Adoption": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of energy consumption derived from renewable sources. Units: Percentage (%)."
                },
                "Energy Efficiency Improvements": {
                    "type": "number",
                    "nullable": True,
                    "description": "Reduction in energy consumption due to efficiency measures. Units: Percentage (%)."
                },
                "Electrification of Operations": {
                    "type": "number",
                    "nullable": True,
                    "description": "Extent to which operations have shifted from fossil fuels to electric power. Units: Percentage (%)."
                },
                "Carbon Capture and Storage (CCS) Implementation": {
                    "type": "number",
                    "nullable": True,
                    "description": "Amount of CO₂ captured and stored to prevent atmospheric release. Units: Metric Tons CO₂e."
                },
                "Reforestation and Afforestation Initiatives": {
                    "type": "number",
                    "nullable": True,
                    "description": "Efforts to plant trees to absorb CO₂ from the atmosphere. Units: Number of Trees Planted or Hectares."
                },
                "Sustainable Transportation Adoption": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of transportation utilizing low-emission or electric vehicles. Units: Percentage (%)."
                },
                "Supply Chain Emissions Reduction": {
                    "type": "number",
                    "nullable": True,
                    "description": "Decrease in emissions from upstream and downstream supply chain activities. Units: Metric Tons CO₂e."
                },
                "Waste-to-Energy Conversion": {
                    "type": "number",
                    "nullable": True,
                    "description": "Energy produced from the processing of waste materials. Units: MWh or GJ."
                },
                "Carbon Offset Investments": {
                    "type": "number",
                    "nullable": True,
                    "description": "Amount of emissions offset through investments in environmental projects. Units: Metric Tons CO₂e."
                },
                "Climate Risk Assessment": {
                    "type": "string",
                    "nullable": True,
                    "description": "Evaluation of potential risks posed by climate change to the organization."
                },
                "Climate Adaptation Strategies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Plans implemented to adapt operations to changing climate conditions."
                },
                "Internal Carbon Pricing": {
                    "type": "number",
                    "nullable": True,
                    "description": "Monetary value assigned to carbon emissions to incentivize reduction. Units: Currency per Metric Ton CO₂e."
                },
                "Net-Zero Target Year": {
                    "type": "string",
                    "nullable": True,
                    "description": "Specific year by which the organization aims to achieve net-zero emissions. Units: Year."
                },
                "Interim Emission Reduction Targets": {
                    "type": "number",
                    "nullable": True,
                    "description": "Short-term targets set to progressively reduce emissions en route to net-zero. Units: Percentage (%)."
                },
                "Employee Engagement in Sustainability": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of employees actively involved in sustainability programs. Units: Percentage (%)."
                },
                "Investment in Low-Carbon Technologies": {
                    "type": "number",
                    "nullable": True,
                    "description": "Financial resources allocated to developing or adopting low-carbon technologies. Units: Currency."
                },
                "Public Disclosure of Net-Zero Progress": {
                    "type": "string",
                    "nullable": True,
                    "description": "Regular public updates on progress toward net-zero commitments."
                },
                "Third-Party Verification of Emission Data": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Confirmation that emission data has been verified by an external party."
                },
                "Participation in Carbon Markets": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Involvement in systems where carbon credits are bought and sold."
                },
                "Development of Climate-Resilient Infrastructure": {
                    "type": "string",
                    "nullable": True,
                    "description": "Initiatives to build infrastructure resilient to climate impacts."
                },
                "Reduction of Methane Emissions": {
                    "type": "number",
                    "nullable": True,
                    "description": "Efforts to decrease methane emissions from operations. Units: Metric Tons CH₄."
                },
                "Implementation of Circular Economy Practices": {
                    "type": "string",
                    "nullable": True,
                    "description": "Adoption of processes that emphasize reuse and recycling to minimize waste."
                },
                "Collaboration with Industry Peers on Climate Action": {
                    "type": "string",
                    "nullable": True,
                    "description": "Joint initiatives with other organizations to address climate challenges."
                },
                "Use of Science-Based Targets": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Setting emission reduction targets in line with scientific recommendations."
                },
                "Monitoring and Reporting Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems established to track and report emissions data accurately."
                }
            },
            "propertyOrdering": [
                "Renewable Energy Adoption",
                "Energy Efficiency Improvements",
                "Electrification of Operations",
                "Carbon Capture and Storage (CCS) Implementation",
                "Reforestation and Afforestation Initiatives",
                "Sustainable Transportation Adoption",
                "Supply Chain Emissions Reduction",
                "Waste-to-Energy Conversion",
                "Carbon Offset Investments",
                "Climate Risk Assessment",
                "Climate Adaptation Strategies",
                "Internal Carbon Pricing",
                "Net-Zero Target Year",
                "Interim Emission Reduction Targets",
                "Employee Engagement in Sustainability",
                "Investment in Low-Carbon Technologies",
                "Public Disclosure of Net-Zero Progress",
                "Third-Party Verification of Emission Data",
                "Participation in Carbon Markets",
                "Development of Climate-Resilient Infrastructure",
                "Reduction of Methane Emissions",
                "Implementation of Circular Economy Practices",
                "Collaboration with Industry Peers on Climate Action",
                "Use of Science-Based Targets",
                "Monitoring and Reporting Mechanisms"
            ]
        }
    
    },
    "propertyOrdering": ["Company Name", "Net Zero Intervention Parameters"]
}

FULL_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "Company Name": {
        "type": "string",
        "description": "Name of the company."
        },
        "Greenhouse Gas (GHG) Protocol Parameters": {
        "type": "object",
        "properties": {
            "Total GHG Emissions": { "type": "integer", "nullable": True, "description": "Total greenhouse gases emitted by the organization. Units: Metric Tons CO₂e." },
            "Scope 1 Emissions": { "type": "integer", "nullable": True, "description": "Direct GHG emissions from owned or controlled sources. Units: Metric Tons CO₂e." },
            "Scope 2 Emissions": { "type": "integer", "nullable": True, "description": "Indirect GHG emissions from the consumption of purchased electricity, steam, heating, and cooling. Units: Metric Tons CO₂e." },
            "Scope 3 Emissions": { "type": "integer", "nullable": True, "description": "Other indirect emissions occurring in the value chain, including both upstream and downstream emissions. Units: Metric Tons CO₂e." },
            "CO₂ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of carbon dioxide. Units: Metric Tons CO₂." },
            "CH₄ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of methane. Units: Metric Tons CH₄." },
            "N₂O Emissions": { "type": "integer", "nullable": True, "description": "Emissions of nitrous oxide. Units: Metric Tons N₂O." },
            "HFC Emissions": { "type": "integer", "nullable": True, "description": "Emissions of hydrofluorocarbons. Units: Metric Tons HFCs" },
            "PFC Emissions": { "type": "integer", "nullable": True, "description": "Emissions of perfluorocarbons. Units: Metric Tons PFCs" },
            "SF₆ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of sulfur hexafluoride. Units: Metric Tons SF₆." },
            "NF₃ Emissions": { "type": "integer", "nullable": True, "description": "Emissions of nitrogen trifluoride. Units: Metric Tons NF₃." },
            "Biogenic CO₂ Emissions": { "type": "integer", "nullable": True, "description": "CO₂ emissions from biological sources. Units: Metric Tons CO₂." },
            "Emissions Intensity per Revenue": { "type": "number", "nullable": True, "description": "GHG emissions per unit of revenue. Units: Metric Tons CO₂e / Revenue." },
            "Emissions Intensity per Employee": { "type": "number", "nullable": True, "description": "GHG emissions per employee. Units: Metric Tons CO₂e / Employee." },
            "Base Year Emissions": { "type": "integer", "nullable": True, "description": "GHG emissions in the base year for comparison. Units: Metric Tons CO₂e." },
            "Emissions Reduction Target": { "type": "number", "nullable": True, "description": "Targeted percentage reduction in GHG emissions. Units: Percentage (%)." },
            "Emissions Reduction Achieved": { "type": "number", "nullable": True, "description": "Actual percentage reduction in GHG emissions achieved. Units: Percentage (%)." },
            "Energy Consumption": { "type": "number", "nullable": True, "description": "Total energy consumed by the organization. Units: MWh or GJ." },
            "Renewable Energy Consumption": { "type": "number", "nullable": True, "description": "Amount of energy consumed from renewable sources. Units: MWh or GJ." },
            "Non-Renewable Energy Consumption": { "type": "number", "nullable": True, "description": "Amount of energy consumed from non-renewable sources. Units: MWh or GJ." },
            "Energy Intensity per Revenue": { "type": "number", "nullable": True, "description": "Energy consumption per unit of revenue. Units: MWh or GJ / Revenue." },
            "Energy Intensity per Employee": { "type": "number", "nullable": True, "description": "Energy consumption per employee. Units: MWh or GJ / Employee." },
            "Fuel Consumption": { "type": "number", "nullable": True, "description": "Total fuel consumed by the organization. Units: Liters or GJ." },
            "Electricity Consumption": { "type": "number", "nullable": True, "description": "Total electricity consumed. Units: MWh." },
            "Heat Consumption": { "type": "number", "nullable": True, "description": "Total heat energy consumed. Units: GJ." },
            "Steam Consumption": { "type": "number", "nullable": True, "description": "Total steam energy consumed. Units: GJ." },
            "Cooling Consumption": { "type": "number", "nullable": True, "description": "Total energy consumed for cooling. Units: GJ." },
            "Purchased Goods and Services Emissions": { "type": "integer", "nullable": True, "description": "Emissions from purchased goods and services. Units: Metric Tons CO₂e." },
            "Capital Goods Emissions": { "type": "integer", "nullable": True, "description": "Emissions from the production of capital goods. Units: Metric Tons CO₂e." },
            "Fuel- and Energy-Related Activities Emissions": { "type": "integer", "nullable": True, "description": "Emissions related to fuel and energy production not included in Scope 1 or 2. Units: Metric Tons CO₂e." },
            "Upstream Transportation and Distribution Emissions": { "type": "integer", "nullable": True, "description": "Emissions from transportation and distribution in the supply chain. Units: Metric Tons CO₂e." },
            "Waste Generated in Operations Emissions": { "type": "integer", "nullable": True, "description": "Emissions from waste generated during operations. Units: Metric Tons CO₂e." },
            "Business Travel Emissions": { "type": "integer", "nullable": True, "description": "Emissions from employee business travel. Units: Metric Tons CO₂e." },
            "Employee Commuting Emissions": { "type": "integer", "nullable": True, "description": "Emissions from employees commuting to and from work. Units: Metric Tons CO₂e." },
            "Upstream Leased Assets Emissions": { "type": "integer", "nullable": True, "description": "Emissions from leased assets upstream in the value chain. Units: Metric Tons CO₂e." },
            "Downstream Transportation and Distribution Emissions": { "type": "integer", "nullable": True, "description": "Emissions from transportation and distribution of sold products. Units: Metric Tons CO₂e." },
            "Processing of Sold Products Emissions": { "type": "integer", "nullable": True, "description": "Emissions from processing intermediate products sold by the organization. Units: Metric Tons CO₂e." },
            "Use of Sold Products Emissions": { "type": "integer", "nullable": True, "description": "Emissions from the use of sold products by consumers. Units: Metric Tons CO₂e." },
            "End-of-Life Treatment of Sold Products Emissions": { "type": "integer", "nullable": True, "description": "Emissions from the disposal of sold products at end of life. Units: Metric Tons CO₂e." },
            "Downstream Leased Assets Emissions": { "type": "integer", "nullable": True, "description": "Emissions from leased assets downstream in the value chain. Units: Metric Tons CO₂e." },
            "Franchises Emissions": { "type": "integer", "nullable": True, "description": "Emissions from franchise operations. Units: Metric Tons CO₂e." },
            "Investments Emissions": { "type": "integer", "nullable": True, "description": "Emissions from investments. Units: Metric Tons CO₂e." },
            "Carbon Offsets Purchased": { "type": "integer", "nullable": True, "description": "Amount of carbon offsets purchased. Units: Metric Tons CO₂e." },
            "Net GHG Emissions": { "type": "integer", "nullable": True, "description": "GHG emissions after accounting for offsets. Units: Metric Tons CO₂e." },
            "Carbon Sequestration": { "type": "integer", "nullable": True, "description": "Amount of CO₂ sequestered or captured. Units: Metric Tons CO₂e." }
        },
        "propertyOrdering": [
            "Total GHG Emissions", "Scope 1 Emissions", "Scope 2 Emissions", "Scope 3 Emissions", "CO₂ Emissions",
            "CH₄ Emissions", "N₂O Emissions", "HFC Emissions", "PFC Emissions", "SF₆ Emissions", "NF₃ Emissions",
            "Biogenic CO₂ Emissions", "Emissions Intensity per Revenue", "Emissions Intensity per Employee",
            "Base Year Emissions", "Emissions Reduction Target", "Emissions Reduction Achieved", "Energy Consumption",
            "Renewable Energy Consumption", "Non-Renewable Energy Consumption", "Energy Intensity per Revenue",
            "Energy Intensity per Employee", "Fuel Consumption", "Electricity Consumption", "Heat Consumption",
            "Steam Consumption", "Cooling Consumption", "Purchased Goods and Services Emissions", "Capital Goods Emissions",
            "Fuel- and Energy-Related Activities Emissions", "Upstream Transportation and Distribution Emissions",
            "Waste Generated in Operations Emissions", "Business Travel Emissions", "Employee Commuting Emissions",
            "Upstream Leased Assets Emissions", "Downstream Transportation and Distribution Emissions",
            "Processing of Sold Products Emissions", "Use of Sold Products Emissions", "End-of-Life Treatment of Sold Products Emissions",
            "Downstream Leased Assets Emissions", "Franchises Emissions", "Investments Emissions", "Carbon Offsets Purchased", "Net GHG Emissions",
            "Carbon Sequestration"
        ]
        },
        "Environmental Parameters (CSRD)": {
            "type": "object",
            "properties": {
                "Environmental Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies related to environmental management and sustainability."
                },
                "Environmental Management System (EMS)": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Existence of an environmental management system."
                },
                "Environmental Certifications": {
                    "type": "string",
                    "nullable": True,
                    "description": "Certifications related to environmental standards."
                }
            },
            "propertyOrdering": [
                "Environmental Policies",
                "Environmental Management System (EMS)",
                "Environmental Certifications"
            ]
        },
        "Environmental Parameters": {
            "type": "object",
            "properties": {
                "Air Emissions": {
                    "type": "integer", "nullable": True, "description": "Total emissions of pollutants into the air. Units: Metric Tons."
                },
                "Water Withdrawal": {
                    "type": "integer", "nullable": True, "description": "Total volume of water extracted from all sources. Units: Cubic Meters."
                },
                "Water Discharge": {
                    "type": "integer", "nullable": True, "description": "Total volume of water discharged back into the environment. Units: Cubic Meters."
                },
                "Waste Generation": {
                    "type": "integer", "nullable": True, "description": "Total amount of waste generated by the organization. Units: Metric Tons."
                },
                "Hazardous Waste": {
                    "type": "integer", "nullable": True, "description": "Amount of waste classified as hazardous. Units: Metric Tons."
                },
                "Non-Hazardous Waste": {
                    "type": "integer", "nullable": True, "description": "Amount of waste not classified as hazardous. Units: Metric Tons."
                },
                "Recycled Waste": {
                    "type": "integer", "nullable": True, "description": "Amount of waste diverted from landfills through recycling. Units: Metric Tons."
                },
                "Energy Consumption": {
                    "type": "number", "nullable": True, "description": "Total energy consumed by the organization. Units: MWh or GJ."
                },
                "Renewable Energy Consumption": {
                    "type": "number", "nullable": True, "description": "Amount of energy consumed from renewable sources. Units: MWh or GJ."
                },
                "Non-Renewable Energy Consumption": {
                    "type": "number", "nullable": True, "description": "Amount of energy consumed from non-renewable sources. Units: MWh or GJ."
                },
                "Energy Intensity": {
                    "type": "number", "nullable": True, "description": "Energy consumption per unit of output or revenue. Units: MWh or GJ per unit."
                },
                "Water Intensity": {
                    "type": "number", "nullable": True, "description": "Water consumption per unit of output or revenue. Units: Cubic Meters per unit."
                },
                "Biodiversity Impact": {
                    "type": "string", "nullable": True, "description": "Description of the organization's impact on biodiversity."
                },
                "Environmental Fines": {
                    "type": "number", "nullable": True, "description": "Total monetary value of fines for environmental violations. Units: Currency."
                },
                "Environmental Investments": {
                    "type": "number", "nullable": True, "description": "Total investments in environmental protection measures. Units: Currency."
                },
                "Environmental Certifications": {
                    "type": "string", "nullable": True, "description": "Certifications related to environmental standards (e.g., ISO 14001)."
                },
                "Environmental Management System (EMS)": {
                    "type": "boolean", "nullable": True, "description": "Existence of an environmental management system."
                },
                "Climate Change Risks": {
                    "type": "string", "nullable": True, "description": "Description of risks related to climate change affecting the organization."
                },
                "Climate Change Opportunities": {
                    "type": "string", "nullable": True, "description": "Description of opportunities related to climate change for the organization."
                },
                "Emissions Reduction Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at reducing GHG emissions."
                },
                "Renewable Energy Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives to increase the use of renewable energy sources."
                },
                "Water Conservation Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at reducing water consumption."
                },
                "Waste Reduction Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at reducing waste generation."
                },
                "Circular Economy Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives promoting the reuse and recycling of materials."
                },
                "Sustainable Sourcing Policies": {
                    "type": "string", "nullable": True, "description": "Policies ensuring procurement of sustainable materials."
                },
                "Supplier Environmental Assessment": {
                    "type": "string", "nullable": True, "description": "Assessment of suppliers' environmental practices."
                },
                "Product Environmental Footprint": {
                    "type": "string", "nullable": True, "description": "Environmental impact assessment of products."
                },
                "Packaging Environmental Impact": {
                    "type": "string", "nullable": True, "description": "Environmental impact of product packaging."
                },
                "Transportation Environmental Impact": {
                    "type": "string", "nullable": True, "description": "Environmental impact of transportation and logistics."
                },
                "Environmental Training Programs": {
                    "type": "string", "nullable": True, "description": "Training programs focused on environmental awareness."
                },
                "Environmental Grievance Mechanisms": {
                    "type": "string", "nullable": True, "description": "Mechanisms for stakeholders to report environmental concerns."
                },
                "Environmental Compliance": {
                    "type": "boolean", "nullable": True, "description": "Adherence to environmental laws and regulations."
                },
                "Environmental Goals and Targets": {
                    "type": "string", "nullable": True, "description": "Specific environmental performance goals set by the organization."
                },
                "Environmental Performance Monitoring": {
                    "type": "string", "nullable": True, "description": "Systems in place to monitor environmental performance."
                },
                "Environmental Reporting": {
                    "type": "string", "nullable": True, "description": "Public reporting of environmental performance and initiatives."
                },
                "Environmental Stakeholder Engagement": {
                    "type": "string", "nullable": True, "description": "Engagement with stakeholders on environmental matters."
                },
                "Environmental Risk Assessment": {
                    "type": "string", "nullable": True, "description": "Assessment of environmental risks associated with operations."
                },
                "Environmental Impact Assessments": {
                    "type": "string", "nullable": True, "description": "Studies conducted to assess environmental impacts of projects."
                },
                "Environmental Restoration Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at restoring damaged ecosystems."
                },
                "Environmental Advocacy and Partnerships": {
                    "type": "string", "nullable": True, "description": "Participation in environmental advocacy and partnerships."
                },
                "Environmental Awards and Recognitions": {
                    "type": "string", "nullable": True, "description": "Awards received for environmental performance."
                }
            },
            "propertyOrdering": ["Air Emissions", "Water Withdrawal", "Water Discharge", "Waste Generation",
            "Hazardous Waste",
            "Non-Hazardous Waste",
            "Recycled Waste",
            "Energy Consumption",
            "Renewable Energy Consumption",
            "Non-Renewable Energy Consumption",
            "Energy Intensity",
            "Water Intensity",
            "Biodiversity Impact",
            "Environmental Fines",
            "Environmental Investments",
            "Environmental Certifications",
            "Environmental Management System (EMS)",
            "Climate Change Risks",
            "Climate Change Opportunities",
            "Emissions Reduction Initiatives",
            "Renewable Energy Initiatives",
            "Water Conservation Initiatives",
            "Waste Reduction Initiatives",
            "Circular Economy Initiatives",
            "Sustainable Sourcing Policies",
            "Supplier Environmental Assessment",
            "Product Environmental Footprint",
            "Packaging Environmental Impact",
            "Transportation Environmental Impact",
            "Environmental Training Programs",
            "Environmental Grievance Mechanisms",
            "Environmental Compliance",
            "Environmental Goals and Targets",
            "Environmental Performance Monitoring",
            "Environmental Reporting",
            "Environmental Stakeholder Engagement",
            "Environmental Risk Assessment",
            "Environmental Impact Assessments",
            "Environmental Restoration Initiatives",
            "Environmental Advocacy and Partnerships",
            "Environmental Awards and Recognitions"
              ]
        },
        "Social Parameters": {
            "type": "object",
            "properties": {
                "Total Workforce": {
                    "type": "integer", "nullable": True, "description": "Total number of employees in the organization. Units: Number of Employees."
                },
                "Employee Turnover Rate": {
                    "type": "number", "nullable": True, "description": "Percentage of employees leaving the organization over a period. Units: Percentage (%)."
                },
                "Gender Diversity": {
                    "type": "number", "nullable": True, "description": "Proportion of male and female employees. Units: Percentage (%)."
                },
                "Employee Training Hours": {
                    "type": "number", "nullable": True, "description": "Total hours spent on employee training. Units: Hours."
                },
                "Health and Safety Incidents": {
                    "type": "integer", "nullable": True, "description": "Total number of health and safety incidents reported. Units: Number of Incidents."
                },
                "Lost Time Injury Rate (LTIR)": {
                    "type": "number", "nullable": True, "description": "Number of injuries resulting in lost work time per million hours worked. Units: Number of Injuries per Million Hours Worked."
                },
                "Employee Engagement Score": {
                    "type": "number", "nullable": True, "description": "Measure of employee engagement and satisfaction. Units: Score."
                },
                "Collective Bargaining Coverage": {
                    "type": "number", "nullable": True, "description": "Percentage of employees covered by collective bargaining agreements. Units: Percentage (%)."
                },
                "Human Rights Policies": {
                    "type": "string", "nullable": True, "description": "Policies related to the protection of human rights within the organization."
                },
                "Supplier Social Assessment": {
                    "type": "string", "nullable": True, "description": "Assessment of suppliers' social practices."
                },
                "Community Engagement Initiatives": {
                    "type": "string", "nullable": True, "description": "Initiatives aimed at engaging and supporting local communities."
                },
                "Customer Satisfaction Score": {
                    "type": "number", "nullable": True, "description": "Measure of customer satisfaction with the organization's products or services. Units: Score."
                },
                "Product Safety Incidents": {
                    "type": "integer", "nullable": True, "description": "Total number of product safety incidents reported. Units: Number of Incidents."
                },
                "Data Privacy Breaches": {
                    "type": "integer", "nullable": True, "description": "Total number of data privacy breaches reported. Units: Number of Breaches."
                },
                "Non-Discrimination Policies": {
                    "type": "string", "nullable": True, "description": "Policies ensuring non-discrimination."
                }
            },
            "propertyOrdering": [
                "Total Workforce",
                "Employee Turnover Rate",
                "Gender Diversity",
                "Employee Training Hours",
                "Health and Safety Incidents",
                "Lost Time Injury Rate (LTIR)",
                "Employee Engagement Score",
                "Collective Bargaining Coverage",
                "Human Rights Policies",
                "Supplier Social Assessment",
                "Community Engagement Initiatives",
                "Customer Satisfaction Score",
                "Product Safety Incidents",
                "Data Privacy Breaches",
                "Non-Discrimination Policies"
            ]
        },
        "Governance Parameters": {
            "type": "object",
            "properties": {
                "Board Composition": {
                    "type": "string",
                    "nullable": True,
                    "description": "Details about the structure of the board, including the number of executive and non-executive directors."
                },
                "Board Diversity": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of board members by gender, ethnicity, or other diversity metrics. Units: Percentage (%)."
                },
                "Independent Directors": {
                    "type": "number",
                    "nullable": True,
                    "description": "Number or percentage of directors who are independent of the company's management. Units: Number or Percentage (%)."
                },
                "Board Committees": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on existing board committees such as audit, remuneration, and nomination committees."
                },
                "Executive Compensation": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total compensation awarded to executives, including salary, bonuses, and stock options. Units: Currency."
                },
                "CEO Pay Ratio": {
                    "type": "number",
                    "nullable": True,
                    "description": "Ratio of CEO compensation to the median employee compensation. Units: Ratio."
                },
                "Succession Planning": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies and procedures in place for executive succession planning."
                },
                "Shareholder Rights": {
                    "type": "string",
                    "nullable": True,
                    "description": "Description of shareholder voting rights and any restrictions."
                },
                "Ownership Structure": {
                    "type": "string",
                    "nullable": True,
                    "description": "Breakdown of ownership by major shareholders, institutional investors, etc."
                },
                "Anti-Corruption Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies and measures implemented to prevent corruption and bribery within the organization."
                },
                "Whistleblower Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems in place for employees and stakeholders to report unethical behavior anonymously."
                },
                "Risk Management Framework": {
                    "type": "string",
                    "nullable": True,
                    "description": "Description of the organization's approach to identifying and managing risks."
                },
                "Compliance with Laws and Regulations": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on the company's compliance with relevant laws and regulations."
                },
                "Political Contributions": {
                    "type": "number",
                    "nullable": True,
                    "description": "Amount of money contributed to political parties, candidates, or lobbying efforts. Units: Currency."
                },
                "Data Privacy Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies related to the protection of personal and sensitive data."
                },
                "Cybersecurity Measures": {
                    "type": "string",
                    "nullable": True,
                    "description": "Description of measures taken to protect the organization's information systems."
                },
                "Business Ethics Training": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total hours of training provided to employees on business ethics. Units: Number of Hours."
                },
                "Conflicts of Interest Policy": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies addressing how conflicts of interest are managed within the organization."
                },
                "Code of Conduct": {
                    "type": "string",
                    "nullable": True,
                    "description": "Document outlining the principles and standards of behavior expected from employees and management."
                },
                "Transparency in Financial Reporting": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on the organization's practices for transparent and accurate financial reporting."
                },
                "Tax Transparency": {
                    "type": "string",
                    "nullable": True,
                    "description": "Disclosure of the company's tax strategy and payments in different jurisdictions."
                },
                "Supply Chain Governance": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies and practices governing the ethical behavior of suppliers and contractors."
                },
                "Intellectual Property Rights": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies related to the protection and management of intellectual property."
                },
                "Environmental Governance": {
                    "type": "string",
                    "nullable": True,
                    "description": "Governance structures in place to oversee environmental sustainability initiatives."
                },
                "Social Governance": {
                    "type": "string",
                    "nullable": True,
                    "description": "Governance structures in place to oversee social responsibility initiatives."
                },
                "Stakeholder Engagement Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies outlining how the organization engages with stakeholders."
                },
                "Legal Proceedings": {
                    "type": "string",
                    "nullable": True,
                    "description": "Information on any significant legal proceedings involving the company."
                },
                "Internal Controls": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems and procedures in place to ensure the integrity of financial and accounting information."
                },
                "Auditor Independence": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring the independence of external auditors from the company's management."
                },
                "ESG Reporting": {
                    "type": "string",
                    "nullable": True,
                    "description": "Practices related to the disclosure of environmental, social, and governance performance."
                },
                "Board Evaluation Processes": {
                    "type": "string",
                    "nullable": True,
                    "description": "Procedures for assessing the performance and effectiveness of the board of directors."
                },
                "Remuneration Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies governing the remuneration of executives and other employees."
                },
                "Ethical Sourcing Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring that sourcing of materials and services is conducted ethically."
                },
                "Human Rights Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies outlining the company's commitment to upholding human rights within its operations and supply chain."
                },
                "Diversity and Inclusion Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies promoting diversity and inclusion within the workplace."
                },
                "Incident Reporting Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems for reporting and addressing incidents of non-compliance or unethical behavior."
                },
                "ESG Integration in Strategy": {
                    "type": "string",
                    "nullable": True,
                    "description": "How environmental, social, and governance factors are integrated into the company's overall strategy."
                },
                "Regulatory Compliance Training": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total hours of training provided to employees on regulatory compliance. Units: Number of Hours."
                },
                "Investor Relations Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies governing communication and engagement with investors and shareholders."
                },
                "Crisis Management Plans": {
                    "type": "string",
                    "nullable": True,
                    "description": "Preparedness plans for managing crises that could impact the organization's operations or reputation."
                },
                "Product Responsibility Policies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring that products and services meet safety and quality standards."
                },
                "Legal Compliance Incidents": {
                    "type": "number",
                    "nullable": True,
                    "description": "Number of incidents where the company was found in violation of laws or regulations. Units: Number of Incidents."
                },
                "Ethical Marketing Practices": {
                    "type": "string",
                    "nullable": True,
                    "description": "Policies ensuring that marketing and advertising practices are conducted ethically."
                },
                "ESG Performance Metrics": {
                    "type": "string",
                    "nullable": True,
                    "description": "Key performance indicators used to measure ESG performance."
                },
                "Board Meeting Attendance": {
                    "type": "number",
                    "nullable": True,
                    "description": "Percentage of board meetings attended by each director. Units: Percentage (%)."
                },
                "Shareholder Engagement Activities": {
                    "type": "string",
                    "nullable": True,
                    "description": "Activities undertaken to engage and communicate with shareholders."
                },
                "Legal Fines and Penalties": {
                    "type": "number",
                    "nullable": True,
                    "description": "Total amount paid in fines and penalties for legal or regulatory infractions. Units: Currency."
                },
                "ESG Oversight Responsibility": {
                    "type": "string",
                    "nullable": True,
                    "description": "Identification of board members or committees responsible for ESG oversight."
                }
            },
            "propertyOrdering": [
                "Board Composition",
                "Board Diversity",
                "Independent Directors",
                "Board Committees",
                "Executive Compensation",
                "CEO Pay Ratio",
                "Succession Planning",
                "Shareholder Rights",
                "Ownership Structure",
                "Anti-Corruption Policies",
                "Whistleblower Mechanisms",
                "Risk Management Framework",
                "Compliance with Laws and Regulations",
                "Political Contributions",
                "Data Privacy Policies",
                "Cybersecurity Measures",
                "Business Ethics Training",
                "Conflicts of Interest Policy",
                "Code of Conduct",
                "Transparency in Financial Reporting",
                "Tax Transparency",
                "Supply Chain Governance",
                "Intellectual Property Rights",
                "Environmental Governance",
                "Social Governance",
                "Stakeholder Engagement Policies",
                "Legal Proceedings",
                "Internal Controls",
                "Auditor Independence",
                "ESG Reporting",
                "Board Evaluation Processes",
                "Remuneration Policies",
                "Ethical Sourcing Policies",
                "Human Rights Policies",
                "Diversity and Inclusion Policies",
                "Incident Reporting Mechanisms",
                "ESG Integration in Strategy",
                "Regulatory Compliance Training",
                "Investor Relations Policies",
                "Crisis Management Plans",
                "Product Responsibility Policies",
                "Legal Compliance Incidents",
                "Ethical Marketing Practices",
                "ESG Performance Metrics",
                "Board Meeting Attendance",
                "Shareholder Engagement Activities",
                "Legal Fines and Penalties",
                "ESG Oversight Responsibility"
            ]
        },
        "Materiality Parameters": {
            "type": "object",
            "properties": {
                "Stakeholder Engagement Level": {
                    "type": "number",
                    "nullable": True,
                    "description": "Degree to which stakeholders are involved in organizational activities or decisions. Units: Number or Percentage (%)."
                },
                "Stakeholder Feedback Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems in place for stakeholders to provide feedback to the organization."
                },
                "Identification of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Process of determining the most significant environmental, social, and governance issues relevant to the organization."
                },
                "Prioritization of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Ranking of identified material issues based on their significance to stakeholders and the organization."
                },
                "Double Materiality Assessment": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Evaluation considering both the organization's impact on sustainability matters and the impact of sustainability matters on the organization."
                },
                "Materiality Matrix Development": {
                    "type": "string",
                    "nullable": True,
                    "description": "Creation of a visual representation (matrix) plotting material issues based on their importance to stakeholders and the organization."
                },
                "Regular Review of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Frequency and process for updating the assessment of material issues."
                },
                "Integration of Material Issues into Strategy": {
                    "type": "string",
                    "nullable": True,
                    "description": "How identified material issues are incorporated into the organization's strategic planning."
                },
                "Disclosure of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Public reporting on identified material issues and how they are managed."
                },
                "Impact Assessment of Material Issues": {
                    "type": "string",
                    "nullable": True,
                    "description": "Analysis of the potential or actual impact of material issues on the organization and its stakeholders."
                }
            },
            "propertyOrdering": [
                "Stakeholder Engagement Level",
                "Stakeholder Feedback Mechanisms",
                "Identification of Material Issues",
                "Prioritization of Material Issues",
                "Double Materiality Assessment",
                "Materiality Matrix Development",
                "Regular Review of Material Issues",
                "Integration of Material Issues into Strategy",
                "Disclosure of Material Issues",
                "Impact Assessment of Material Issues"
            ]
        },
        "Net Zero Intervention Parameters": {
            "type": "object",
            "properties": {
                "Renewable Energy Adoption": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of energy consumption derived from renewable sources. Units: Percentage (%)."
                },
                "Energy Efficiency Improvements": {
                    "type": "number",
                    "nullable": True,
                    "description": "Reduction in energy consumption due to efficiency measures. Units: Percentage (%)."
                },
                "Electrification of Operations": {
                    "type": "number",
                    "nullable": True,
                    "description": "Extent to which operations have shifted from fossil fuels to electric power. Units: Percentage (%)."
                },
                "Carbon Capture and Storage (CCS) Implementation": {
                    "type": "number",
                    "nullable": True,
                    "description": "Amount of CO₂ captured and stored to prevent atmospheric release. Units: Metric Tons CO₂e."
                },
                "Reforestation and Afforestation Initiatives": {
                    "type": "number",
                    "nullable": True,
                    "description": "Efforts to plant trees to absorb CO₂ from the atmosphere. Units: Number of Trees Planted or Hectares."
                },
                "Sustainable Transportation Adoption": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of transportation utilizing low-emission or electric vehicles. Units: Percentage (%)."
                },
                "Supply Chain Emissions Reduction": {
                    "type": "number",
                    "nullable": True,
                    "description": "Decrease in emissions from upstream and downstream supply chain activities. Units: Metric Tons CO₂e."
                },
                "Waste-to-Energy Conversion": {
                    "type": "number",
                    "nullable": True,
                    "description": "Energy produced from the processing of waste materials. Units: MWh or GJ."
                },
                "Carbon Offset Investments": {
                    "type": "number",
                    "nullable": True,
                    "description": "Amount of emissions offset through investments in environmental projects. Units: Metric Tons CO₂e."
                },
                "Climate Risk Assessment": {
                    "type": "string",
                    "nullable": True,
                    "description": "Evaluation of potential risks posed by climate change to the organization."
                },
                "Climate Adaptation Strategies": {
                    "type": "string",
                    "nullable": True,
                    "description": "Plans implemented to adapt operations to changing climate conditions."
                },
                "Internal Carbon Pricing": {
                    "type": "number",
                    "nullable": True,
                    "description": "Monetary value assigned to carbon emissions to incentivize reduction. Units: Currency per Metric Ton CO₂e."
                },
                "Net-Zero Target Year": {
                    "type": "string",
                    "nullable": True,
                    "description": "Specific year by which the organization aims to achieve net-zero emissions. Units: Year."
                },
                "Interim Emission Reduction Targets": {
                    "type": "number",
                    "nullable": True,
                    "description": "Short-term targets set to progressively reduce emissions en route to net-zero. Units: Percentage (%)."
                },
                "Employee Engagement in Sustainability": {
                    "type": "number",
                    "nullable": True,
                    "description": "Proportion of employees actively involved in sustainability programs. Units: Percentage (%)."
                },
                "Investment in Low-Carbon Technologies": {
                    "type": "number",
                    "nullable": True,
                    "description": "Financial resources allocated to developing or adopting low-carbon technologies. Units: Currency."
                },
                "Public Disclosure of Net-Zero Progress": {
                    "type": "string",
                    "nullable": True,
                    "description": "Regular public updates on progress toward net-zero commitments."
                },
                "Third-Party Verification of Emission Data": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Confirmation that emission data has been verified by an external party."
                },
                "Participation in Carbon Markets": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Involvement in systems where carbon credits are bought and sold."
                },
                "Development of Climate-Resilient Infrastructure": {
                    "type": "string",
                    "nullable": True,
                    "description": "Initiatives to build infrastructure resilient to climate impacts."
                },
                "Reduction of Methane Emissions": {
                    "type": "number",
                    "nullable": True,
                    "description": "Efforts to decrease methane emissions from operations. Units: Metric Tons CH₄."
                },
                "Implementation of Circular Economy Practices": {
                    "type": "string",
                    "nullable": True,
                    "description": "Adoption of processes that emphasize reuse and recycling to minimize waste."
                },
                "Collaboration with Industry Peers on Climate Action": {
                    "type": "string",
                    "nullable": True,
                    "description": "Joint initiatives with other organizations to address climate challenges."
                },
                "Use of Science-Based Targets": {
                    "type": "boolean",
                    "nullable": True,
                    "description": "Setting emission reduction targets in line with scientific recommendations."
                },
                "Monitoring and Reporting Mechanisms": {
                    "type": "string",
                    "nullable": True,
                    "description": "Systems established to track and report emissions data accurately."
                }
            },
            "propertyOrdering": [
                "Renewable Energy Adoption",
                "Energy Efficiency Improvements",
                "Electrification of Operations",
                "Carbon Capture and Storage (CCS) Implementation",
                "Reforestation and Afforestation Initiatives",
                "Sustainable Transportation Adoption",
                "Supply Chain Emissions Reduction",
                "Waste-to-Energy Conversion",
                "Carbon Offset Investments",
                "Climate Risk Assessment",
                "Climate Adaptation Strategies",
                "Internal Carbon Pricing",
                "Net-Zero Target Year",
                "Interim Emission Reduction Targets",
                "Employee Engagement in Sustainability",
                "Investment in Low-Carbon Technologies",
                "Public Disclosure of Net-Zero Progress",
                "Third-Party Verification of Emission Data",
                "Participation in Carbon Markets",
                "Development of Climate-Resilient Infrastructure",
                "Reduction of Methane Emissions",
                "Implementation of Circular Economy Practices",
                "Collaboration with Industry Peers on Climate Action",
                "Use of Science-Based Targets",
                "Monitoring and Reporting Mechanisms"
            ]
        }
    },
    "propertyOrdering": [   "Company Name", "Greenhouse Gas (GHG) Protocol Parameters", "Environmental Parameters (CSRD)", 
                            "Environmental Parameters",
                            "Social Parameters", "Governance Parameters", "Materiality Parameters",
                            "Net Zero Intervention Parameters"
                            ]
}

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "esg_response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "company_name": {"type": "string"},
                "Greenhouse Gas (GHG) Protocol Parameters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "Total GHG Emissions": {"type": ["integer", "null"]},
                            "Total GHG Emissions Description": {
                                "type": "string",
                                "description": "Total greenhouse gases emitted by the organization."
                            },
                            "Scope 1 Emissions": {"type": ["integer", "null"]},
                            "Scope 1 Emissions Description": {
                                "type": "string",
                                "description": "Direct GHG emissions from owned or controlled sources."
                            },
                            "Scope 2 Emissions": {"type": ["integer", "null"]},
                            "Scope 2 Emissions Description": {
                                "type": "string",
                                "description": "Indirect emissions from the generation of purchased electricity."
                            },
                            "Scope 3 Emissions": {"type": ["integer", "null"]},
                            "Scope 3 Emissions Description": {
                                "type": "string",
                                "description": "All other indirect emissions that occur in a company’s value chain."
                            },
                            "CO₂ Emissions": {"type": ["integer", "null"]},
                            "CO₂ Emissions Description": {
                                "type": "string",
                                "description": "Emissions of carbon dioxide."
                            },
                            "CH₄ Emissions": {"type": ["integer", "null"]},
                            "CH₄ Emissions Description": {
                                "type": "string",
                                "description": "Emissions of methane."
                            },
                            "N₂O Emissions": {"type": ["integer", "null"]},
                            "N₂O Emissions Description": {
                                "type": "string",
                                "description": "Emissions of nitrous oxide."
                            },
                            "HFC Emissions": {"type": ["integer", "null"]},
                            "HFC Emissions Description": {
                                "type": "string",
                                "description": "Emissions of hydrofluorocarbons."
                            },
                            "PFC Emissions": {"type": ["integer", "null"]},
                            "PFC Emissions Description": {
                                "type": "string",
                                "description": "Emissions of perfluorocarbons."
                            }
                        },
                        "required": [
                            "Total GHG Emissions", "Total GHG Emissions Description",
                            "Scope 1 Emissions", "Scope 1 Emissions Description",
                            "Scope 2 Emissions", "Scope 2 Emissions Description",
                            "Scope 3 Emissions", "Scope 3 Emissions Description",
                            "CO₂ Emissions", "CO₂ Emissions Description",
                            "CH₄ Emissions", "CH₄ Emissions Description",
                            "N₂O Emissions", "N₂O Emissions Description",
                            "HFC Emissions", "HFC Emissions Description",
                            "PFC Emissions", "PFC Emissions Description"
                        ],
                        "additionalProperties": False
                    }
                },

                "Net Zero Intervention Parameters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "Renewable Energy Adoption": {"type": ["number", "null"]},
                            "Renewable Energy Adoption Description": {
                                "type": "string",
                                "description": "Proportion of energy consumption derived from renewable sources."
                            },
                            "Energy Efficiency Improvements": {"type": ["number", "null"]},
                            "Energy Efficiency Improvements Description": {
                                "type": "string",
                                "description": "Reduction in energy consumption due to efficiency measures."
                            },
                            "Electrification of Operations": {"type": ["number", "null"]},
                            "Electrification of Operations Description": {
                                "type": "string",
                                "description": "Extent to which operations have shifted from fossil fuels to electric power."
                            },
                            "Carbon Capture and Storage (CCS) Implementation": {"type": ["number", "null"]},
                            "Carbon Capture and Storage (CCS) Implementation Description": {
                                "type": "string",
                                "description": "Amount of CO₂ captured and stored to prevent atmospheric release."
                            },
                            "Reforestation and Afforestation Initiatives": {"type": ["number", "null"]},
                            "Reforestation and Afforestation Initiatives Description": {
                                "type": "string",
                                "description": "Efforts to plant trees to absorb CO₂ from the atmosphere."
                            },
                            "Sustainable Transportation Adoption": {"type": ["number", "null"]},
                            "Sustainable Transportation Adoption Description": {
                                "type": "string",
                                "description": "Proportion of transportation utilizing low-emission or electric vehicles."
                            },
                            "Supply Chain Emissions Reduction": {"type": ["number", "null"]},
                            "Supply Chain Emissions Reduction Description": {
                                "type": "string",
                                "description": "Decrease in emissions from upstream and downstream supply chain activities."
                            },
                            "Waste-to-Energy Conversion": {"type": ["number", "null"]},
                            "Waste-to-Energy Conversion Description": {
                                "type": "string",
                                "description": "Energy produced from the processing of waste materials."
                            },
                            "Carbon Offset Investments": {"type": ["number", "null"]},
                            "Carbon Offset Investments Description": {
                                "type": "string",
                                "description": "Amount of emissions offset through investments in environmental projects."
                            },
                            "Climate Risk Assessment": {"type": ["string", "null"]},
                            "Climate Risk Assessment Description": {
                                "type": "string",
                                "description": "Evaluation of potential risks posed by climate change to the organization."
                            },
                            "Climate Adaptation Strategies": {"type": ["string", "null"]},
                            "Climate Adaptation Strategies Description": {
                                "type": "string",
                                "description": "Plans implemented to adapt operations to changing climate conditions."
                            },
                            "Internal Carbon Pricing": {"type": ["number", "null"]},
                            "Internal Carbon Pricing Description": {
                                "type": "string",
                                "description": "Monetary value assigned to carbon emissions to incentivize reduction."
                            },
                            "Net-Zero Target Year": {"type": ["string", "null"]},
                            "Net-Zero Target Year Description": {
                                "type": "string",
                                "description": "Specific year by which the organization aims to achieve net-zero emissions."
                            },
                            "Interim Emission Reduction Targets": {"type": ["number", "null"]},
                            "Interim Emission Reduction Targets Description": {
                                "type": "string",
                                "description": "Short-term targets set to progressively reduce emissions en route to net-zero."
                            },
                            "Employee Engagement in Sustainability": {"type": ["number", "null"]},
                            "Employee Engagement in Sustainability Description": {
                                "type": "string",
                                "description": "Proportion of employees actively involved in sustainability programs."
                            },
                            "Investment in Low-Carbon Technologies": {"type": ["number", "null"]},
                            "Investment in Low-Carbon Technologies Description": {
                                "type": "string",
                                "description": "Financial resources allocated to developing or adopting low-carbon technologies."
                            },
                            "Public Disclosure of Net-Zero Progress": {"type": ["string", "null"]},
                            "Public Disclosure of Net-Zero Progress Description": {
                                "type": "string",
                                "description": "Regular public updates on progress toward net-zero commitments."
                            },
                            "Third-Party Verification of Emission Data": {"type": ["boolean", "null"]},
                            "Third-Party Verification of Emission Data Description": {
                                "type": "string",
                                "description": "Confirmation that emission data has been verified by an external party."
                            },
                            "Participation in Carbon Markets": {"type": ["boolean", "null"]},
                            "Participation in Carbon Markets Description": {
                                "type": "string",
                                "description": "Involvement in systems where carbon credits are bought and sold."
                            },
                            "Development of Climate-Resilient Infrastructure": {"type": ["string", "null"]},
                            "Development of Climate-Resilient Infrastructure Description": {
                                "type": "string",
                                "description": "Initiatives to build infrastructure resilient to climate impacts."
                            },
                            "Reduction of Methane Emissions": {"type": ["number", "null"]},
                            "Reduction of Methane Emissions Description": {
                                "type": "string",
                                "description": "Efforts to decrease methane emissions from operations."
                            },
                            "Implementation of Circular Economy Practices": {"type": ["string", "null"]},
                            "Implementation of Circular Economy Practices Description": {
                                "type": "string",
                                "description": "Adoption of processes that emphasize reuse and recycling to minimize waste."
                            },
                            "Collaboration with Industry Peers on Climate Action": {"type": ["string", "null"]},
                            "Collaboration with Industry Peers on Climate Action Description": {
                                "type": "string",
                                "description": "Joint initiatives with other organizations to address climate challenges."
                            },
                            "Use of Science-Based Targets": {"type": ["boolean", "null"]},
                            "Use of Science-Based Targets Description": {
                                "type": "string",
                                "description": "Setting emission reduction targets in line with scientific recommendations."
                            },
                            "Monitoring and Reporting Mechanisms": {"type": ["string", "null"]},
                            "Monitoring and Reporting Mechanisms Description": {
                                "type": "string",
                                "description": "Systems established to track and report emissions data accurately."
                            }
                        },
                        "required": [
                            "Renewable Energy Adoption", "Renewable Energy Adoption Description",
                            "Energy Efficiency Improvements", "Energy Efficiency Improvements Description",
                            "Electrification of Operations", "Electrification of Operations Description",
                            "Carbon Capture and Storage (CCS) Implementation", "Carbon Capture and Storage (CCS) Implementation Description",
                            "Reforestation and Afforestation Initiatives", "Reforestation and Afforestation Initiatives Description",
                            "Sustainable Transportation Adoption", "Sustainable Transportation Adoption Description",
                            "Supply Chain Emissions Reduction", "Supply Chain Emissions Reduction Description",
                            "Waste-to-Energy Conversion", "Waste-to-Energy Conversion Description",
                            "Carbon Offset Investments", "Carbon Offset Investments Description",
                            "Climate Risk Assessment", "Climate Risk Assessment Description",
                            "Climate Adaptation Strategies", "Climate Adaptation Strategies Description",
                            "Internal Carbon Pricing", "Internal Carbon Pricing Description",
                            "Net-Zero Target Year", "Net-Zero Target Year Description",
                            "Interim Emission Reduction Targets", "Interim Emission Reduction Targets Description",
                            "Employee Engagement in Sustainability", "Employee Engagement in Sustainability Description",
                            "Investment in Low-Carbon Technologies", "Investment in Low-Carbon Technologies Description",
                            "Public Disclosure of Net-Zero Progress", "Public Disclosure of Net-Zero Progress Description",
                            "Third-Party Verification of Emission Data", "Third-Party Verification of Emission Data Description",
                            "Participation in Carbon Markets", "Participation in Carbon Markets Description",
                            "Development of Climate-Resilient Infrastructure", "Development of Climate-Resilient Infrastructure Description",
                            "Reduction of Methane Emissions", "Reduction of Methane Emissions Description",
                            "Implementation of Circular Economy Practices", "Implementation of Circular Economy Practices Description",
                            "Collaboration with Industry Peers on Climate Action", "Collaboration with Industry Peers on Climate Action Description",
                            "Use of Science-Based Targets", "Use of Science-Based Targets Description",
                            "Monitoring and Reporting Mechanisms", "Monitoring and Reporting Mechanisms Description"
                        ],
                        "additionalProperties": False
                    }
                },
                
                "Materiality Parameters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "Stakeholder Engagement Level": {
                                "type": ["string", "null"]
                            },
                            "Stakeholder Engagement Level Description": {
                                "type": "string",
                                "description": "Degree to which stakeholders are involved in organizational activities or decisions."
                            },
                            "Stakeholder Feedback Mechanisms": {
                                "type": ["string", "null"]
                            },
                            "Stakeholder Feedback Mechanisms Description": {
                                "type": "string",
                                "description": "Systems in place for stakeholders to provide feedback to the organization."
                            },
                            "Identification of Material Issues": {
                                "type": ["string", "null"]
                            },
                            "Identification of Material Issues Description": {
                                "type": "string",
                                "description": "Process of determining the most significant environmental, social, and governance issues relevant to the organization."
                            },
                            "Prioritization of Material Issues": {
                                "type": ["string", "null"]
                            },
                            "Prioritization of Material Issues Description": {
                                "type": "string",
                                "description": "Ranking of identified material issues based on their significance to stakeholders and the organization."
                            },
                            "Double Materiality Assessment": {
                                "type": ["string", "null"]
                            },
                            "Double Materiality Assessment Description": {
                                "type": "string",
                                "description": "Evaluation considering both the organization's impact on sustainability matters and the impact of those matters on the organization."
                            },
                            "Materiality Matrix Development": {
                                "type": ["string", "null"]
                            },
                            "Materiality Matrix Development Description": {
                                "type": "string",
                                "description": "Creation of a visual matrix plotting material issues based on their importance to stakeholders and the organization."
                            },
                            "Regular Review of Material Issues": {
                                "type": ["string", "null"]
                            },
                            "Regular Review of Material Issues Description": {
                                "type": "string",
                                "description": "Frequency and process for updating the assessment of material issues."
                            },
                            "Integration of Material Issues into Strategy": {
                                "type": ["string", "null"]
                            },
                            "Integration of Material Issues into Strategy Description": {
                                "type": "string",
                                "description": "How identified material issues are incorporated into the organization's strategic planning."
                            },
                            "Disclosure of Material Issues": {
                                "type": ["string", "null"]
                            },
                            "Disclosure of Material Issues Description": {
                                "type": "string",
                                "description": "Public reporting on identified material issues and how they are managed."
                            },
                            "Impact Assessment of Material Issues": {
                                "type": ["string", "null"]
                            },
                            "Impact Assessment of Material Issues Description": {
                                "type": "string",
                                "description": "Analysis of the potential or actual impact of material issues on the organization and its stakeholders."
                            }
                        },
                        "required": [
                            "Stakeholder Engagement Level",
                            "Stakeholder Engagement Level Description",
                            "Stakeholder Feedback Mechanisms",
                            "Stakeholder Feedback Mechanisms Description",
                            "Identification of Material Issues",
                            "Identification of Material Issues Description",
                            "Prioritization of Material Issues",
                            "Prioritization of Material Issues Description",
                            "Double Materiality Assessment",
                            "Double Materiality Assessment Description",
                            "Materiality Matrix Development",
                            "Materiality Matrix Development Description",
                            "Regular Review of Material Issues",
                            "Regular Review of Material Issues Description",
                            "Integration of Material Issues into Strategy",
                            "Integration of Material Issues into Strategy Description",
                            "Disclosure of Material Issues",
                            "Disclosure of Material Issues Description",
                            "Impact Assessment of Material Issues",
                            "Impact Assessment of Material Issues Description"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["company_name", "Greenhouse Gas (GHG) Protocol Parameters", "Net Zero Intervention Parameters", "Materiality Parameters"],
            "additionalProperties": False
        }
    }
}

SECTOR_AND_REGION_SCHEMA = {
    "type": "object",
    "properties": {
        "Company Name": {
            "type": "string",
            "description": "The full legal name of the company.",
        },
        "Sector": {
            "type": "string",
            "description": "The primary industry or sector the company operates in (e.g., 'Technology', 'Energy', 'Healthcare').",
        },
        "Region": {
            "type": "string",
            "description": "The primary geographic region where the company is headquartered or has major operations (e.g., 'North America', 'Europe', 'Asia-Pacific', 'Global').",
        },
    },
    "required": ["Company Name", "Sector", "Region"],
}

ENHANCED_COMPANY_REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "Company Name": {
            "type": "string",
            "description": "The full legal name of the company."
        },
        "Industry (GICS)": {
            "type": "string",
            "description": "GICS industry classification based on MSCI definitions"
        },
        "Sector (GICS)": {
            "type": "string",
            "description": "GICS sector classification based on MSCI definitions"
        },
        "Headquarters": {
            "type": "string",
            "description": "The city and country where the company is headquartered."
        },
        "Peer Region(s)": {
            "type": "string",
            "description": "Region classification (e.g., 'North America', 'Europe', 'Asia-Pacific', etc.)"
        },
        "Report Years": {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^\\d{4}$"
            },
            "description": "List of years for which reports are provided."
        },
        "Report Type(s)": {
                "type": "string",
                "description": "List of applicable report types published by the company. (e.g., 'ESG Report', 'Sustainability Report', 'Integrated Report', ESG Dashboard) or 'N/A'."
            },
    },
    "required": [
        "Company Name",
        "Industry (GICS)",
        "Sector (GICS)",
        "Headquarters",
        "Peer Region(s)",
        "Report Years",
        "Report Type(s)",
    ]
}


class GreenhouseGasProtocolParameters(BaseModel):
    total_ghg_emissions: Optional[int] = Field(None, description="Total greenhouse gases emitted by the organization. Units: Metric Tons CO₂e.")
    scope_1_emissions: Optional[int] = Field(None, description="Direct GHG emissions from owned or controlled sources. Units: Metric Tons CO₂e.")
    scope_2_emissions: Optional[int] = Field(None, description="Indirect GHG emissions from the consumption of purchased electricity, steam, heating, and cooling. Units: Metric Tons CO₂e.")
    scope_3_emissions: Optional[int] = Field(None, description="Other indirect emissions occurring in the value chain, including both upstream and downstream emissions. Units: Metric Tons CO₂e.")
    co2_emissions: Optional[int] = Field(None, description="Emissions of carbon dioxide. Units: Metric Tons CO₂.")
    ch4_emissions: Optional[int] = Field(None, description="Emissions of methane. Units: Metric Tons CH₄.")
    n2o_emissions: Optional[int] = Field(None, description="Emissions of nitrous oxide. Units: Metric Tons N₂O.")
    hfc_emissions: Optional[int] = Field(None, description="Emissions of hydrofluorocarbons. Units: Metric Tons HFCs.")
    pfc_emissions: Optional[int] = Field(None, description="Emissions of perfluorocarbons. Units: Metric Tons PFCs.")
    sf6_emissions: Optional[int] = Field(None, description="Emissions of sulfur hexafluoride. Units: Metric Tons SF₆.")
    nf3_emissions: Optional[int] = Field(None, description="Emissions of nitrogen trifluoride. Units: Metric Tons NF₃.")
    biogenic_co2_emissions: Optional[int] = Field(None, description="CO₂ emissions from biological sources. Units: Metric Tons CO₂.")
    emissions_intensity_per_revenue: Optional[float] = Field(None, description="GHG emissions per unit of revenue. Units: Metric Tons CO₂e / Revenue.")
    emissions_intensity_per_employee: Optional[float] = Field(None, description="GHG emissions per employee. Units: Metric Tons CO₂e / Employee.")
    base_year_emissions: Optional[int] = Field(None, description="GHG emissions in the base year for comparison. Units: Metric Tons CO₂e.")
    emissions_reduction_target: Optional[float] = Field(None, description="Targeted percentage reduction in GHG emissions. Units: Percentage (%).")
    emissions_reduction_achieved: Optional[float] = Field(None, description="Actual percentage reduction in GHG emissions achieved. Units: Percentage (%).")
    energy_consumption: Optional[float] = Field(None, description="Total energy consumed by the organization. Units: MWh or GJ.")
    renewable_energy_consumption: Optional[float] = Field(None, description="Amount of energy consumed from renewable sources. Units: MWh or GJ.")
    non_renewable_energy_consumption: Optional[float] = Field(None, description="Amount of energy consumed from non-renewable sources. Units: MWh or GJ.")
    energy_intensity_per_revenue: Optional[float] = Field(None, description="Energy consumption per unit of revenue. Units: MWh or GJ / Revenue.")
    energy_intensity_per_employee: Optional[float] = Field(None, description="Energy consumption per employee. Units: MWh or GJ / Employee.")
    fuel_consumption: Optional[float] = Field(None, description="Total fuel consumed by the organization. Units: Liters or GJ.")
    electricity_consumption: Optional[float] = Field(None, description="Total electricity consumed. Units: MWh.")
    heat_consumption: Optional[float] = Field(None, description="Total heat energy consumed. Units: GJ.")
    steam_consumption: Optional[float] = Field(None, description="Total steam energy consumed. Units: GJ.")
    cooling_consumption: Optional[float] = Field(None, description="Total energy consumed for cooling. Units: GJ.")
    purchased_goods_and_services_emissions: Optional[int] = Field(None, description="Emissions from purchased goods and services. Units: Metric Tons CO₂e.")
    capital_goods_emissions: Optional[int] = Field(None, description="Emissions from the production of capital goods. Units: Metric Tons CO₂e.")
    fuel_and_energy_related_activities_emissions: Optional[int] = Field(None, description="Emissions related to fuel and energy production not included in Scope 1 or 2. Units: Metric Tons CO₂e.")
    upstream_transportation_and_distribution_emissions: Optional[int] = Field(None, description="Emissions from transportation and distribution in the supply chain. Units: Metric Tons CO₂e.")
    waste_generated_in_operations_emissions: Optional[int] = Field(None, description="Emissions from waste generated during operations. Units: Metric Tons CO₂e.")
    business_travel_emissions: Optional[int] = Field(None, description="Emissions from employee business travel. Units: Metric Tons CO₂e.")
    employee_commuting_emissions: Optional[int] = Field(None, description="Emissions from employees commuting to and from work. Units: Metric Tons CO₂e.")
    upstream_leased_assets_emissions: Optional[int] = Field(None, description="Emissions from leased assets upstream in the value chain. Units: Metric Tons CO₂e.")
    downstream_transportation_and_distribution_emissions: Optional[int] = Field(None, description="Emissions from transportation and distribution of sold products. Units: Metric Tons CO₂e.")
    processing_of_sold_products_emissions: Optional[int] = Field(None, description="Emissions from processing intermediate products sold by the organization. Units: Metric Tons CO₂e.")
    use_of_sold_products_emissions: Optional[int] = Field(None, description="Emissions from the use of sold products by consumers. Units: Metric Tons CO₂e.")
    end_of_life_treatment_of_sold_products_emissions: Optional[int] = Field(None, description="Emissions from the disposal of sold products at end of life. Units: Metric Tons CO₂e.")
    downstream_leased_assets_emissions: Optional[int] = Field(None, description="Emissions from leased assets downstream in the value chain. Units: Metric Tons CO₂e.")
    franchises_emissions: Optional[int] = Field(None, description="Emissions from franchise operations. Units: Metric Tons CO₂e.")
    investments_emissions: Optional[int] = Field(None, description="Emissions from investments. Units: Metric Tons CO₂e.")
    carbon_offsets_purchased: Optional[int] = Field(None, description="Amount of carbon offsets purchased. Units: Metric Tons CO₂e.")
    net_ghg_emissions: Optional[int] = Field(None, description="GHG emissions after accounting for offsets. Units: Metric Tons CO₂e.")
    carbon_sequestration: Optional[int] = Field(None, description="Amount of CO₂ sequestered or captured. Units: Metric Tons CO₂e.")

class EnvironmentalParametersCSRD(BaseModel):
    environmental_policies: Optional[str] = Field(
        None, description="Policies related to environmental management and sustainability."
    )
    environmental_management_system_ems: Optional[bool] = Field(
        None, description="Existence of an environmental management system."
    )
    environmental_certifications: Optional[str] = Field(
        None, description="Certifications related to environmental standards."
    )

class EnvironmentalParameters(BaseModel):
    air_emissions: Optional[int] = Field(None, description="Total emissions of pollutants into the air. Units: Metric Tons.")
    water_withdrawal: Optional[int] = Field(None, description="Total volume of water extracted from all sources. Units: Cubic Meters.")
    water_discharge: Optional[int] = Field(None, description="Total volume of water discharged back into the environment. Units: Cubic Meters.")
    waste_generation: Optional[int] = Field(None, description="Total amount of waste generated by the organization. Units: Metric Tons.")
    hazardous_waste: Optional[int] = Field(None, description="Amount of waste classified as hazardous. Units: Metric Tons.")
    non_hazardous_waste: Optional[int] = Field(None, description="Amount of waste not classified as hazardous. Units: Metric Tons.")
    recycled_waste: Optional[int] = Field(None, description="Amount of waste diverted from landfills through recycling. Units: Metric Tons.")
    energy_consumption: Optional[float] = Field(None, description="Total energy consumed by the organization. Units: MWh or GJ.")
    renewable_energy_consumption: Optional[float] = Field(None, description="Amount of energy consumed from renewable sources. Units: MWh or GJ.")
    non_renewable_energy_consumption: Optional[float] = Field(None, description="Amount of energy consumed from non-renewable sources. Units: MWh or GJ.")
    energy_intensity: Optional[float] = Field(None, description="Energy consumption per unit of output or revenue. Units: MWh or GJ per unit.")
    water_intensity: Optional[float] = Field(None, description="Water consumption per unit of output or revenue. Units: Cubic Meters per unit.")
    biodiversity_impact: Optional[str] = Field(None, description="Description of the organization's impact on biodiversity.")
    environmental_fines: Optional[float] = Field(None, description="Total monetary value of fines for environmental violations. Units: Currency.")
    environmental_investments: Optional[float] = Field(None, description="Total investments in environmental protection measures. Units: Currency.")
    environmental_certifications: Optional[str] = Field(None, description="Certifications related to environmental standards (e.g., ISO 14001).")
    environmental_management_system_ems: Optional[bool] = Field(None, description="Existence of an environmental management system.")
    climate_change_risks: Optional[str] = Field(None, description="Description of risks related to climate change affecting the organization.")
    climate_change_opportunities: Optional[str] = Field(None, description="Description of opportunities related to climate change for the organization.")
    emissions_reduction_initiatives: Optional[str] = Field(None, description="Initiatives aimed at reducing GHG emissions.")
    renewable_energy_initiatives: Optional[str] = Field(None, description="Initiatives to increase the use of renewable energy sources.")
    water_conservation_initiatives: Optional[str] = Field(None, description="Initiatives aimed at reducing water consumption.")
    waste_reduction_initiatives: Optional[str] = Field(None, description="Initiatives aimed at reducing waste generation.")
    circular_economy_initiatives: Optional[str] = Field(None, description="Initiatives promoting the reuse and recycling of materials.")
    sustainable_sourcing_policies: Optional[str] = Field(None, description="Policies ensuring procurement of sustainable materials.")
    supplier_environmental_assessment: Optional[str] = Field(None, description="Assessment of suppliers' environmental practices.")
    product_environmental_footprint: Optional[str] = Field(None, description="Environmental impact assessment of products.")
    packaging_environmental_impact: Optional[str] = Field(None, description="Environmental impact of product packaging.")
    transportation_environmental_impact: Optional[str] = Field(None, description="Environmental impact of transportation and logistics.")
    environmental_training_programs: Optional[str] = Field(None, description="Training programs focused on environmental awareness.")
    environmental_grievance_mechanisms: Optional[str] = Field(None, description="Mechanisms for stakeholders to report environmental concerns.")
    environmental_compliance: Optional[bool] = Field(None, description="Adherence to environmental laws and regulations.")
    environmental_goals_and_targets: Optional[str] = Field(None, description="Specific environmental performance goals set by the organization.")
    environmental_performance_monitoring: Optional[str] = Field(None, description="Systems in place to monitor environmental performance.")
    environmental_reporting: Optional[str] = Field(None, description="Public reporting of environmental performance and initiatives.")
    environmental_stakeholder_engagement: Optional[str] = Field(None, description="Engagement with stakeholders on environmental matters.")
    environmental_risk_assessment: Optional[str] = Field(None, description="Assessment of environmental risks associated with operations.")
    environmental_impact_assessments: Optional[str] = Field(None, description="Studies conducted to assess environmental impacts of projects.")
    environmental_restoration_initiatives: Optional[str] = Field(None, description="Initiatives aimed at restoring damaged ecosystems.")
    environmental_advocacy_and_partnerships: Optional[str] = Field(None, description="Participation in environmental advocacy and partnerships.")
    environmental_awards_and_recognitions: Optional[str] = Field(None, description="Awards received for environmental performance.")

class SocialParameters(BaseModel):
    total_workforce: Optional[int] = Field(
        None, description="Total number of employees in the organization. Units: Number of Employees."
    )
    employee_turnover_rate: Optional[float] = Field(
        None, description="Percentage of employees leaving the organization over a period. Units: Percentage (%)."
    )
    gender_diversity: Optional[float] = Field(
        None, description="Proportion of male and female employees. Units: Percentage (%)."
    )
    employee_training_hours: Optional[float] = Field(
        None, description="Total hours spent on employee training. Units: Hours."
    )
    health_and_safety_incidents: Optional[int] = Field(
        None, description="Total number of health and safety incidents reported. Units: Number of Incidents."
    )
    lost_time_injury_rate_ltir: Optional[float] = Field(
        None, description="Number of injuries resulting in lost work time per million hours worked. Units: Number of Injuries per Million Hours Worked."
    )
    employee_engagement_score: Optional[float] = Field(
        None, description="Measure of employee engagement and satisfaction. Units: Score."
    )
    collective_bargaining_coverage: Optional[float] = Field(
        None, description="Percentage of employees covered by collective bargaining agreements. Units: Percentage (%)."
    )
    human_rights_policies: Optional[str] = Field(
        None, description="Policies related to the protection of human rights within the organization."
    )
    supplier_social_assessment: Optional[str] = Field(
        None, description="Assessment of suppliers' social practices."
    )
    community_engagement_initiatives: Optional[str] = Field(
        None, description="Initiatives aimed at engaging and supporting local communities."
    )
    customer_satisfaction_score: Optional[float] = Field(
        None, description="Measure of customer satisfaction with the organization's products or services. Units: Score."
    )
    product_safety_incidents: Optional[int] = Field(
        None, description="Total number of product safety incidents reported. Units: Number of Incidents."
    )
    data_privacy_breaches: Optional[int] = Field(
        None, description="Total number of data privacy breaches reported. Units: Number of Breaches."
    )
    non_discrimination_policies: Optional[str] = Field(
        None, description="Policies ensuring non-discrimination."
    )

class GovernanceParameters(BaseModel):
    Board_Composition: Optional[str] = Field(None, description="Details about the structure of the board, including the number of executive and non-executive directors.")
    Board_Diversity: Optional[float] = Field(None, description="Proportion of board members by gender, ethnicity, or other diversity metrics. Units: Percentage (%).")
    Independent_Directors: Optional[float] = Field(None, description="Number or percentage of directors who are independent of the company's management. Units: Number or Percentage (%).")
    Board_Committees: Optional[str] = Field(None, description="Information on existing board committees such as audit, remuneration, and nomination committees.")
    Executive_Compensation: Optional[float] = Field(None, description="Total compensation awarded to executives, including salary, bonuses, and stock options. Units: Currency.")
    CEO_Pay_Ratio: Optional[float] = Field(None, description="Ratio of CEO compensation to the median employee compensation. Units: Ratio.")
    Succession_Planning: Optional[str] = Field(None, description="Policies and procedures in place for executive succession planning.")
    Shareholder_Rights: Optional[str] = Field(None, description="Description of shareholder voting rights and any restrictions.")
    Ownership_Structure: Optional[str] = Field(None, description="Breakdown of ownership by major shareholders, institutional investors, etc.")
    Anti_Corruption_Policies: Optional[str] = Field(None, description="Policies and measures implemented to prevent corruption and bribery within the organization.")
    Whistleblower_Mechanisms: Optional[str] = Field(None, description="Systems in place for employees and stakeholders to report unethical behavior anonymously.")
    Risk_Management_Framework: Optional[str] = Field(None, description="Description of the organization's approach to identifying and managing risks.")
    Compliance_with_Laws_and_Regulations: Optional[str] = Field(None, description="Information on the company's compliance with relevant laws and regulations.")
    Political_Contributions: Optional[float] = Field(None, description="Amount of money contributed to political parties, candidates, or lobbying efforts. Units: Currency.")
    Data_Privacy_Policies: Optional[str] = Field(None, description="Policies related to the protection of personal and sensitive data.")
    Cybersecurity_Measures: Optional[str] = Field(None, description="Description of measures taken to protect the organization's information systems.")
    Business_Ethics_Training: Optional[float] = Field(None, description="Total hours of training provided to employees on business ethics. Units: Number of Hours.")
    Conflicts_of_Interest_Policy: Optional[str] = Field(None, description="Policies addressing how conflicts of interest are managed within the organization.")
    Code_of_Conduct: Optional[str] = Field(None, description="Document outlining the principles and standards of behavior expected from employees and management.")
    Transparency_in_Financial_Reporting: Optional[str] = Field(None, description="Information on the organization's practices for transparent and accurate financial reporting.")
    Tax_Transparency: Optional[str] = Field(None, description="Disclosure of the company's tax strategy and payments in different jurisdictions.")
    Supply_Chain_Governance: Optional[str] = Field(None, description="Policies and practices governing the ethical behavior of suppliers and contractors.")
    Intellectual_Property_Rights: Optional[str] = Field(None, description="Policies related to the protection and management of intellectual property.")
    Environmental_Governance: Optional[str] = Field(None, description="Governance structures in place to oversee environmental sustainability initiatives.")
    Social_Governance: Optional[str] = Field(None, description="Governance structures in place to oversee social responsibility initiatives.")
    Stakeholder_Engagement_Policies: Optional[str] = Field(None, description="Policies outlining how the organization engages with stakeholders.")
    Legal_Proceedings: Optional[str] = Field(None, description="Information on any significant legal proceedings involving the company.")
    Internal_Controls: Optional[str] = Field(None, description="Systems and procedures in place to ensure the integrity of financial and accounting information.")
    Auditor_Independence: Optional[str] = Field(None, description="Policies ensuring the independence of external auditors from the company's management.")
    ESG_Reporting: Optional[str] = Field(None, description="Practices related to the disclosure of environmental, social, and governance performance.")
    Board_Evaluation_Processes: Optional[str] = Field(None, description="Procedures for assessing the performance and effectiveness of the board of directors.")
    Remuneration_Policies: Optional[str] = Field(None, description="Policies governing the remuneration of executives and other employees.")
    Ethical_Sourcing_Policies: Optional[str] = Field(None, description="Policies ensuring that sourcing of materials and services is conducted ethically.")
    Human_Rights_Policies: Optional[str] = Field(None, description="Policies outlining the company's commitment to upholding human rights within its operations and supply chain.")
    Diversity_and_Inclusion_Policies: Optional[str] = Field(None, description="Policies promoting diversity and inclusion within the workplace.")
    Incident_Reporting_Mechanisms: Optional[str] = Field(None, description="Systems for reporting and addressing incidents of non-compliance or unethical behavior.")
    ESG_Integration_in_Strategy: Optional[str] = Field(None, description="How environmental, social, and governance factors are integrated into the company's overall strategy.")
    Regulatory_Compliance_Training: Optional[float] = Field(None, description="Total hours of training provided to employees on regulatory compliance. Units: Number of Hours.")
    Investor_Relations_Policies: Optional[str] = Field(None, description="Policies governing communication and engagement with investors and shareholders.")
    Crisis_Management_Plans: Optional[str] = Field(None, description="Preparedness plans for managing crises that could impact the organization's operations or reputation.")
    Product_Responsibility_Policies: Optional[str] = Field(None, description="Policies ensuring that products and services meet safety and quality standards.")
    Legal_Compliance_Incidents: Optional[float] = Field(None, description="Number of incidents where the company was found in violation of laws or regulations. Units: Number of Incidents.")
    Ethical_Marketing_Practices: Optional[str] = Field(None, description="Policies ensuring that marketing and advertising practices are conducted ethically.")
    ESG_Performance_Metrics: Optional[str] = Field(None, description="Key performance indicators used to measure ESG performance.")
    Board_Meeting_Attendance: Optional[float] = Field(None, description="Percentage of board meetings attended by each director. Units: Percentage (%).")
    Shareholder_Engagement_Activities: Optional[str] = Field(None, description="Activities undertaken to engage and communicate with shareholders.")
    Legal_Fines_and_Penalties: Optional[float] = Field(None, description="Total amount paid in fines and penalties for legal or regulatory infractions. Units: Currency.")
    ESG_Oversight_Responsibility: Optional[str] = Field(None, description="Identification of board members or committees responsible for ESG oversight.")

class MaterialityParameters(BaseModel):
    Stakeholder_Engagement_Level: Optional[float] = Field(None, description="Degree to which stakeholders are involved in organizational activities or decisions. Units: Number or Percentage (%).")
    Stakeholder_Feedback_Mechanisms: Optional[str] = Field(None, description="Systems in place for stakeholders to provide feedback to the organization.")
    Identification_of_Material_Issues: Optional[str] = Field(None, description="Process of determining the most significant environmental, social, and governance issues relevant to the organization.")
    Prioritization_of_Material_Issues: Optional[str] = Field(None, description="Ranking of identified material issues based on their significance to stakeholders and the organization.")
    Double_Materiality_Assessment: Optional[bool] = Field(None, description="Evaluation considering both the organization's impact on sustainability matters and the impact of sustainability matters on the organization.")
    Materiality_Matrix_Development: Optional[str] = Field(None, description="Creation of a visual representation (matrix) plotting material issues based on their importance to stakeholders and the organization.")
    Regular_Review_of_Material_Issues: Optional[str] = Field(None, description="Frequency and process for updating the assessment of material issues.")
    Integration_of_Material_Issues_into_Strategy: Optional[str] = Field(None, description="How identified material issues are incorporated into the organization's strategic planning.")
    Disclosure_of_Material_Issues: Optional[str] = Field(None, description="Public reporting on identified material issues and how they are managed.")
    Impact_Assessment_of_Material_Issues: Optional[str] = Field(None, description="Analysis of the potential or actual impact of material issues on the organization and its stakeholders.")

class NetZeroInterventionParameters(BaseModel):
    Renewable_Energy_Adoption: Optional[float] = Field(None, description="Proportion of energy consumption derived from renewable sources. Units: Percentage (%).")
    Energy_Efficiency_Improvements: Optional[float] = Field(None, description="Reduction in energy consumption due to efficiency measures. Units: Percentage (%).")
    Electrification_of_Operations: Optional[float] = Field(None, description="Extent to which operations have shifted from fossil fuels to electric power. Units: Percentage (%).")
    Carbon_Capture_and_Storage_CCS_Implementation: Optional[float] = Field(None, description="Amount of CO₂ captured and stored to prevent atmospheric release. Units: Metric Tons CO₂e.")
    Reforestation_and_Afforestation_Initiatives: Optional[float] = Field(None, description="Efforts to plant trees to absorb CO₂ from the atmosphere. Units: Number of Trees Planted or Hectares.")
    Sustainable_Transportation_Adoption: Optional[float] = Field(None, description="Proportion of transportation utilizing low-emission or electric vehicles. Units: Percentage (%).")
    Supply_Chain_Emissions_Reduction: Optional[float] = Field(None, description="Decrease in emissions from upstream and downstream supply chain activities. Units: Metric Tons CO₂e.")
    Waste_to_Energy_Conversion: Optional[float] = Field(None, description="Energy produced from the processing of waste materials. Units: MWh or GJ.")
    Carbon_Offset_Investments: Optional[float] = Field(None, description="Amount of emissions offset through investments in environmental projects. Units: Metric Tons CO₂e.")
    Climate_Risk_Assessment: Optional[str] = Field(None, description="Evaluation of potential risks posed by climate change to the organization.")
    Climate_Adaptation_Strategies: Optional[str] = Field(None, description="Plans implemented to adapt operations to changing climate conditions.")
    Internal_Carbon_Pricing: Optional[float] = Field(None, description="Monetary value assigned to carbon emissions to incentivize reduction. Units: Currency per Metric Ton CO₂e.")
    Net_Zero_Target_Year: Optional[str] = Field(None, description="Specific year by which the organization aims to achieve net-zero emissions. Units: Year.")
    Interim_Emission_Reduction_Targets: Optional[float] = Field(None, description="Short-term targets set to progressively reduce emissions en route to net-zero. Units: Percentage (%).")
    Employee_Engagement_in_Sustainability: Optional[float] = Field(None, description="Proportion of employees actively involved in sustainability programs. Units: Percentage (%).")
    Investment_in_Low_Carbon_Technologies: Optional[float] = Field(None, description="Financial resources allocated to developing or adopting low-carbon technologies. Units: Currency.")
    Public_Disclosure_of_Net_Zero_Progress: Optional[str] = Field(None, description="Regular public updates on progress toward net-zero commitments.")
    Third_Party_Verification_of_Emission_Data: Optional[bool] = Field(None, description="Confirmation that emission data has been verified by an external party.")
    Participation_in_Carbon_Markets: Optional[bool] = Field(None, description="Involvement in systems where carbon credits are bought and sold.")
    Development_of_Climate_Resilient_Infrastructure: Optional[str] = Field(None, description="Initiatives to build infrastructure resilient to climate impacts.")
    Reduction_of_Methane_Emissions: Optional[float] = Field(None, description="Efforts to decrease methane emissions from operations. Units: Metric Tons CH₄.")
    Implementation_of_Circular_Economy_Practices: Optional[str] = Field(None, description="Adoption of processes that emphasize reuse and recycling to minimize waste.")
    Collaboration_with_Industry_Peers_on_Climate_Action: Optional[str] = Field(None, description="Joint initiatives with other organizations to address climate challenges.")
    Use_of_Science_Based_Targets: Optional[bool] = Field(None, description="Setting emission reduction targets in line with scientific recommendations.")
    Monitoring_and_Reporting_Mechanisms: Optional[str] = Field(None, description="Systems established to track and report emissions data accurately.")

class GHGParameters(BaseModel):
    company_name: str = Field(..., alias="Company Name", description="Name of the company.")
    greenhouse_gas_protocol_parameters: GreenhouseGasProtocolParameters = Field(..., alias="Greenhouse Gas (GHG) Protocol Parameters")
    environmental_parameters_csrd: EnvironmentalParametersCSRD = Field(..., alias="Environmental Parameters (CSRD)")
    environmental_parameters: EnvironmentalParameters = Field(..., alias="Environmental Parameters")

class GHGParameters2(BaseModel):
    # social_parameters: SocialParameters = Field(..., alias="Social Parameters")
    # governance_parameters: GovernanceParameters = Field(..., alias="Governance Parameters")
    materiality_parameters: MaterialityParameters = Field(..., alias="Materiality Parameters")

class GHGParameters3(BaseModel):
    netzero_intervention_parameters: NetZeroInterventionParameters = Field(..., alias="NetZero Intervention Parameters")

class CompanyMetadata(BaseModel):
    company_name: str = Field(..., description="The full legal name of the company.")
    industry: str = Field(..., description="GICS industry classification based on MSCI definitions (e.g., 'Software', 'Pharmaceuticals').")
    sector: str = Field(..., description=" GICS sector classification based on MSCI definitions (e.g., 'Information Technology', 'Health Care').")
    headquarters: str = Field(..., description="The city and country where the company is headquartered.")
    region: str = Field(..., description="The region considered (e.g., 'North America', 'Europe', 'Asia-Pacific') or 'N/A'.")