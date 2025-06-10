from pydantic import BaseModel, Field
from typing import Optional, List, Union

class Measurement(BaseModel):
    """
    A standardized representation of a quantitative metric with its unit.
    Numeric values support int or float.
    """
    numeric_value: Optional[Union[float, int]] = Field(
        None,
        description="Numerical value of the measurement."
    )
    measurement_unit: Optional[str] = Field(
        None,
        description="Unit of measurement for the numeric value."
    )

class IntensityMetrics(BaseModel):
    intensity_per_revenue: Optional[Measurement] = Field(
        None,
        description="Metric intensity per unit revenue in INR."
    )
    intensity_per_unit: Optional[Measurement] = Field(
        None,
        description="Metric intensity per production/performance unit."
    )

class ReportDetails(BaseModel):
    """
    Contains metadata related to an ESG (Environmental, Social, and Governance) report.

    This model captures key attributes such as the issuing company's legal name, the reporting year,
    and framework details. It also includes publication-related information like the report's title,
    URL, file format, and release dates. These fields help ensure transparency and traceability of
    ESG disclosures and support compliance with global sustainability reporting standards.
    """

    company_legal_name: str = Field(
        ...,
        description="The full legal name of the company or organization issuing the ESG report.",
        example="GreenFuture Technologies Inc."
    )
    reporting_year: int = Field(
        ...,
        description="The calendar or fiscal year to which the ESG data pertains.",
        example=2024
    )
    report_title: Optional[str] = Field(
        None,
        description="Title of the ESG or sustainability report.",
        example="2024 ESG and Sustainability Report"
    )
    report_url: Optional[str] = Field(
        None,
        description="Direct URL to view or download the ESG report.",
        example="https://www.company.com/reports/esg2024.pdf"
    )
    report_release_date: Optional[str] = Field(
        None,
        description="The official release date of the ESG report in YYYY-MM-DD format.",
        example="2025-03-31"
    )
    reporting_framework: Optional[str] = Field(
        None,
        description="The ESG reporting standard or framework followed (e.g., GRI, SASB, TCFD, ESRS).",
        example="GRI Standards 2021"
    )

# __________________________Environmental Metrics___________________________________________

class EmissionDetails(BaseModel):
    """
    GHG emissions measured in tCO₂e, intensity measured in INR.
    """
    total_emissions: Optional[Measurement] = Field(
        None,
        description="Total GHG emissions (Scope 1 + 2 + 3) in metric tons CO₂ equivalent (tCO₂e).",
        alias="Total Emissions"
    )
    scope_1_emissions: Optional[Measurement] = Field(
        None,
        description="Scope 1 direct emissions in tCO₂e.",
        alias="Scope 1 Emissions"
    )
    scope_2_emissions: Optional[Measurement] = Field(
        None,
        description="Scope 2 indirect emissions in tCO₂e.",
        alias="Scope 2 Emissions"
    )
    scope_3_emissions: Optional[Measurement] = Field(
        None,
        description="Scope 3 other indirect emissions in tCO₂e.",
        alias="Scope 3 Emissions"
    )
    # intensity_per_revenue: Optional[Measurement] = Field(
    #     None,
    #     description="Emission intensity per unit revenue, in Indian Rupees (INR).",
    #     example={"numeric_value": 25.3, "measurement_unit": "INR/tCO₂e"}
    # )
    # intensity_per_unit: Optional[Measurement] = Field(
    #     None,
    #     description="Emission intensity per unit of production/performance, in INR.",
    #     example={"numeric_value": 1.2, "measurement_unit": "INR/tCO₂e"}
    # )

class EnergyDetails(BaseModel):
    """
    Energy consumption measured in Gigajoules (GJ).
    """
    total_energy: Optional[Measurement] = Field(
        None,
        description="Total energy consumption in Gigajoules (GJ).",
        alias="Total Energy"
    )
    electricity: Optional[Measurement] = Field(
        None,
        description="Electricity consumption in Gigajoules (GJ).",
        alias="Electricity"
    )
    fuel: Optional[Measurement] = Field(
        None,
        description="Fuel energy consumption in Gigajoules (GJ).",
        alias="Fuel"
    )
    other_sources: Optional[Measurement] = Field(
        None,
        description="Other energy sources in Gigajoules (GJ).",
        alias="Other Sources"
    )
    # intensity_per_revenue: Optional[Measurement] = Field(
    #     None,
    #     description="Energy consumption intensity per revenue unit in INR.",
    #     example={"numeric_value": 50, "measurement_unit": "INR/GJ"}
    # )
    # intensity_per_unit: Optional[Measurement] = Field(
    #     None,
    #     description="Energy consumption intensity per production/performance unit.",
    #     example={"numeric_value": 5, "measurement_unit": "INR/GJ"}
    # )

class EnergyConsumption(BaseModel):
    renewable_energy: Optional[EnergyDetails] = Field(
        None,
        description="Energy from renewable sources in Gigajoules (GJ).",
        alias="Renewable Energy"
    )
    non_renewable_energy: Optional[EnergyDetails] = Field(
        None,
        description="Energy from non-renewable sources in Gigajoules (GJ).",
        alias="Non-Renewable Energy"
    )

class WaterWithdrawalDetails(BaseModel):
    """
    Detailed breakdown of total water withdrawal from different sources.

    This includes:
    - Surface water: Rivers, lakes, reservoirs, etc.
    - Ground water: Freshwater from underground sources.
    - Third-party water: Purchased or supplied water (e.g., municipal).
    - Sea water: Desalinated or otherwise used marine water.
    - Other sources: Any additional water sources.
    - Intensity metrics per revenue and per production/performance unit.
    """

    total_water_withdrawal: Optional[Measurement] = Field(
        default=None,
        description="Total water withdrawal in kilo-liters (KL).",
        alias="Total Water Withdrawal"
    )
    surface_water: Optional[Measurement] = Field(
        default=None,
        description="Water withdrawn from surface water in KL.",
        alias="Surface Water"
    )
    ground_water: Optional[Measurement] = Field(
        default=None,
        description="Water withdrawn from ground water sources in KL.",
        alias="Ground Water"
    )
    third_party_water: Optional[Measurement] = Field(
        default=None,
        description="Water from third-party sources in KL.",
        alias="Third Party Water"
    )
    sea_water: Optional[Measurement] = Field(
        default=None,
        description="Sea water withdrawn in KL.",
        alias="Sea Water"
    )
    other_sources: Optional[Measurement] = Field(
        default=None,
        description="Water withdrawn from other sources in KL.",
        alias="Other Sources"
    )
    # intensity_per_revenue: Optional[Measurement] = Field(
    #     None,
    #     description="Water withdrawal intensity per unit revenue in INR.",
    #     example={"numeric_value": 75, "measurement_unit": "INR/KL"}
    # )
    # intensity_per_unit: Optional[Measurement] = Field(
    #     None,
    #     description="Water withdrawal intensity per production/performance unit."
    # )

class WaterDischargeDetails(BaseModel):
    """
    Breakdown of total water discharge by destination.

    This includes:
    - Surface water: Discharge into rivers, lakes, etc.
    - Groundwater: Infiltration or injection into underground sources.
    - Third-party: Sent to treatment facilities or reused externally.
    - Sea water: Discharged into marine environments.
    - Other destinations: Not classified above.
    - Intensity metrics per revenue and per production/performance unit.
    """

    total_water_discharged: Optional[Measurement] = Field(
        None,
        description="Total water discharged in kilo-liters (KL).",
    )
    surface_water: Optional[Measurement] = Field(
        None,
        description="Water discharged to surface water in KL."
    )
    ground_water: Optional[Measurement] = Field(
        None,
        description="Water discharged to groundwater in KL."
    )
    third_party: Optional[Measurement] = Field(
        None,
        description="Water discharged to third parties in KL."
    )
    sea_water: Optional[Measurement] = Field(
        None,
        description="Water discharged to sea water in KL."
    )
    other_destinations: Optional[Measurement] = Field(
        None,
        description="Water discharged to other destinations in KL."
    )
    # intensity_per_revenue: Optional[Measurement] = Field(
    #     None,
    #     description="Water discharge intensity per revenue unit in INR.",
    #     example={"numeric_value": 40, "measurement_unit": "INR/KL"}
    # )
    # intensity_per_unit: Optional[Measurement] = Field(
    #     None,
    #     description="Water discharge intensity per production/performance unit."
    # )

class WasteGenerationDetails(BaseModel):
    """
    Breakdown of total waste generated by type, including both hazardous and non-hazardous waste streams.

    Includes:
    - Total waste generated
    - Category-specific waste (e.g., plastic, e-waste, biomedical, etc.)
    - Intensity metrics per revenue and production/performance
    """

    total_waste_generated: Optional[Measurement] = Field(
        None,
        description="Total waste generated in metric tonnes.",
    )
    plastic_waste: Optional[Measurement] = Field(
        None,
        description="Plastic waste generated in metric tonnes."
    )
    e_waste: Optional[Measurement] = Field(
        None,
        description="Electronic waste generated in metric tonnes."
    )
    bio_medical_waste: Optional[Measurement] = Field(
        None,
        description="Bio-medical waste generated in metric tonnes."
    )
    construction_demolition_waste: Optional[Measurement] = Field(
        None,
        description="Construction and demolition waste generated in metric tonnes."
    )
    battery_waste: Optional[Measurement] = Field(
        None,
        description="Battery waste generated in metric tonnes."
    )
    radioactive_waste: Optional[Measurement] = Field(
        None,
        description="Radioactive waste generated in metric tonnes."
    )
    other_hazardous_waste: Optional[Measurement] = Field(
        None,
        description="Other hazardous waste in metric tonnes."
    )
    other_non_hazardous_waste: Optional[Measurement] = Field(
        None,
        description="Other non-hazardous waste in metric tonnes."
    )
    # intensity_per_revenue: Optional[Measurement] = Field(
    #     None,
    #     description="Waste generation intensity per revenue unit in INR.",
    #     example={"numeric_value": 1500, "measurement_unit": "INR/metric tonne"}
    # )
    # intensity_per_unit: Optional[Measurement] = Field(
    #     None,
    #     description="Waste generation intensity per production/performance unit."
    # )

class WasteDisposalDetails(BaseModel):
    """
    Breakdown of total waste disposed by disposal method.

    This includes:
    - Incineration: Waste destroyed by burning.
    - Landfilling: Waste buried in landfill sites.
    - Other methods: Includes composting, recycling, deep well injection, etc.
    """

    total_waste_disposed: Optional[Measurement] = Field(
        None,
        description="Total waste disposed in metric tonnes.",
    )
    incineration: Optional[Measurement] = Field(
        None,
        description="Waste disposed through incineration in metric tonnes."
    )
    landfilling: Optional[Measurement] = Field(
        None,
        description="Waste disposed through landfilling in metric tonnes."
    )
    other_methods: Optional[Measurement] = Field(
        None,
        description="Waste disposed through other methods in metric tonnes."
    )
    # intensity_per_revenue: Optional[Measurement] = Field(
    #     None,
    #     description="Waste disposal intensity per revenue unit in INR.",
    #     example={"numeric_value": 1200, "measurement_unit": "INR/metric tonne"}
    # )
    # intensity_per_unit: Optional[Measurement] = Field(
    #     None,
    #     description="Waste disposal intensity per production/performance unit."
    # )

class WasteRecoveryDetails(BaseModel):
    """
    Breakdown of waste recovered by disposal method.

    This includes:
    - Incineration: Waste treated via combustion, often with energy recovery.
    - Landfilling: Waste disposed of in landfills.
    - Other methods: Any additional recovery methods not specified.
    """

    total_waste_recovered: Optional[Measurement] = Field(
        default=None,
        description="Total waste recovered via all methods combined, in metric tonnes."
    )
    incineration: Optional[Measurement] = Field(
        default=None,
        description="Waste recovered through incineration in metric tonnes."
    )
    landfilling: Optional[Measurement] = Field(
        default=None,
        description="Waste recovered through landfilling in metric tonnes."
    )
    other_methods: Optional[Measurement] = Field(
        default=None,
        description="Waste recovered through other methods in metric tonnes."
    )
    # intensity_per_revenue: Optional[Measurement] = Field(
    #     default=None,
    #     description="Waste recovery intensity normalized per unit of revenue (metric tonnes per million INR)."
    # )
    # intensity_per_unit: Optional[Measurement] = Field(
    #     default=None,
    #     description="Waste recovery intensity normalized per production or performance unit (metric tonnes per unit)."
    # )

# __________________________Scocial Metrics___________________________________________

class WorkforceGenderDiversity(BaseModel):
    """
    Breakdown of workforce by gender.

    This includes:
    - Male: Number of male employees.
    - Female: Number of female employees.
    - Total Employees: Total number of employees.
    """

    total_employees: Optional[Measurement] = Field(
        None,
        description="Total number of employees.",
    )
    male: Optional[Measurement] = Field(
        None,
        description="Number of male employees."
    )
    female: Optional[Measurement] = Field(
        None,
        description="Number of female employees."
    )

class HumanRightsTrainingCoverage(BaseModel):
    """
    Coverage of human rights and policies training.

    This includes:
    - Total permanent employees covered
    - Employees: Office staff, management, etc.
    - Workers: Contractual, field staff, labor, etc.
    """

    total_permanent_covered: Optional[Measurement] = Field(
        None,
        description="Total number of permanent staff covered under human rights and policy training.",
    )
    employee: Optional[Measurement] = Field(
        None,
        description="Number of employees (e.g., office staff, management) covered under training."
    )
    worker: Optional[Measurement] = Field(
        None,
        description="Number of workers (e.g., contractors, labor) covered under training."
    )

class TurnoverCount(BaseModel):
    """
    Employee turnover count by gender.

    This includes:
    - Total employees who left the organization.
    - Male employees who left.
    - Female employees who left.
    """

    total_employee: Optional[Measurement] = Field(
        None,
        description="Total number of employees who left the organization.",
    )
    male: Optional[Measurement] = Field(
        None,
        description="Number of male employees who left."
    )
    female: Optional[Measurement] = Field(
        None,
        description="Number of female employees who left."
    )

class HealthAndSafetyLTIFR(BaseModel):
    """
    Lost Time Injury Frequency Rate (LTIFR) for employees and workers.

    LTIFR is typically defined as the number of lost time injuries per million hours worked.
    """

    employee: Optional[Measurement] = Field(
        None,
        description="LTIFR for employees.",
    )
    worker: Optional[Measurement] = Field(
        None,
        description="LTIFR for workers.",
    )

class IncidentBreakdown(BaseModel):
    total: Optional[Measurement] = Field(
        None,
        description="Total number of incidents (employees + workers)."
    )
    employee: Optional[Measurement] = Field(
        None,
        description="Number of incidents involving employees."
    )
    worker: Optional[Measurement] = Field(
        None,
        description="Number of incidents involving workers."
    )

class OtherHealthAndSafetyIncidents(BaseModel):
    """
    Detailed reporting of other health and safety-related incidents,
    including total and breakdown by employees and workers.

    Covers:
    - Recordable Incidents
    - Fatalities
    - High Consequence Injuries
    """

    recordable_incidents: Optional[IncidentBreakdown] = Field(
        None,
        description="Recordable incidents involving employees and workers."
    )
    fatalities: Optional[IncidentBreakdown] = Field(
        None,
        description="Fatalities involving employees and workers."
    )
    high_consequence_injuries: Optional[IncidentBreakdown] = Field(
        None,
        description="High consequence injuries involving employees and workers."
    )

class HealthAndSafetyTrainingCoverage(BaseModel):
    """
    Coverage of health and safety training by gender.

    Tracks the number of employees who received health and safety training.
    """

    total_employees: Optional[Measurement] = Field(
        None,
        description="Total number of employees who received health and safety training.",
    )
    male: Optional[Measurement] = Field(
        None,
        description="Number of male employees trained."
    )
    female: Optional[Measurement] = Field(
        None,
        description="Number of female employees trained."
    )

class GenderBreakdown(BaseModel):
    total: Optional[Measurement] = Field(
        None, description="Total number of employees covered."
    )
    male: Optional[Measurement] = Field(
        None, description="Number of male employees covered."
    )
    female: Optional[Measurement] = Field(
        None, description="Number of female employees covered."
    )

class EmployeeWellBeingCoverage(BaseModel):
    """
    Coverage of measures for the well-being of employees, broken down by benefit type and gender.
    """

    health_insurance: Optional[GenderBreakdown] = Field(
        None, description="Coverage of health insurance."
    )
    accident_insurance: Optional[GenderBreakdown] = Field(
        None, description="Coverage of accident insurance."
    )
    parental_benefits: Optional[GenderBreakdown] = Field(
        None, description="Coverage of parental benefits."
    )
    day_care_facilities: Optional[GenderBreakdown] = Field(
        None, description="Coverage of day care facilities."
    )

class WorkerWellBeingCoverage(BaseModel):
    """
    Coverage of well-being measures for workers, including health and accident insurance,
    parental benefits, and day care facilities, broken down by gender.
    """

    health_insurance: Optional[GenderBreakdown] = Field(
        None, description="Coverage of health insurance for workers."
    )
    accident_insurance: Optional[GenderBreakdown] = Field(
        None, description="Coverage of accident insurance for workers."
    )
    parental_benefits: Optional[GenderBreakdown] = Field(
        None, description="Coverage of parental benefits for workers."
    )
    day_care_facilities: Optional[GenderBreakdown] = Field(
        None, description="Coverage of day care facilities for workers."
    )

class WellBeingCost(BaseModel):
    """
    Total cost incurred on employee and worker well-being programs,
    optionally broken down by category.
    """

    total_cost: Optional[Measurement] = Field(
        None,
        description="Total cost incurred on all well-being programs."
    )
    health_insurance: Optional[Measurement] = Field(
        None,
        description="Cost incurred on health insurance."
    )
    accident_insurance: Optional[Measurement] = Field(
        None,
        description="Cost incurred on accident insurance."
    )
    parental_benefits: Optional[Measurement] = Field(
        None,
        description="Cost incurred on parental benefits."
    )
    day_care_facilities: Optional[Measurement] = Field(
        None,
        description="Cost incurred on day care facilities."
    )

class WagesByLocation(BaseModel):
    """
    Average wages for employees by location type.
    """
    rural: Optional[Measurement] = Field(None, description="Wages in rural locations.")
    semi_urban: Optional[Measurement] = Field(None, description="Wages in semi-urban locations.")
    metropolitan: Optional[Measurement] = Field(None, description="Wages in metropolitan locations.")
    urban: Optional[Measurement] = Field(None, description="Wages in urban locations.")

class FemaleWageShare(BaseModel):
    """
    Represents the share of wages paid to female employees as a percentage of total wages.
    """
    percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Female wage share as a percentage of total wages."
    )

class GrievanceCategory(BaseModel):
    total_complaints: Optional[int] = Field(
        None, description="Total number of complaints reported."
    )
    resolved: Optional[int] = Field(
        None, description="Number of complaints resolved."
    )
    not_resolved: Optional[int] = Field(
        None, description="Number of complaints not resolved."
    )

class GrievancesReported(BaseModel):
    posh: Optional[GrievanceCategory] = Field(
        None, description="Grievances related to POSH (Prevention of Sexual Harassment)."
    )
    discrimination: Optional[GrievanceCategory] = Field(
        None, description="Grievances related to discrimination."
    )
    health_and_safety: Optional[GrievanceCategory] = Field(
        None, description="Grievances related to health and safety."
    )
    working_conditions: Optional[GrievanceCategory] = Field(
        None, description="Grievances related to working conditions."
    )

class ThirdPartyAssessmentCoveragePercentage(BaseModel):
    """
    Percentage coverage of third party assessments per category.
    Values represent the % of coverage (0-100).
    """

    child_labour: Optional[float] = Field(
        None, ge=0, le=100,
        description="Percentage coverage of third party assessment for child labour."
    )
    forced_involuntary_labour: Optional[float] = Field(
        None, ge=0, le=100,
        description="Percentage coverage of third party assessment for forced/involuntary labour."
    )
    sexual_harassment: Optional[float] = Field(
        None, ge=0, le=100,
        description="Percentage coverage of third party assessment for sexual harassment."
    )
    discrimination_at_workplace: Optional[float] = Field(
        None, ge=0, le=100,
        description="Percentage coverage of third party assessment for discrimination at workplace."
    )
    wages: Optional[float] = Field(
        None, ge=0, le=100,
        description="Percentage coverage of third party assessment for wages."
    )

class BeneficiaryGroup(BaseModel):
    persons_benefited: Optional[int] = Field(
        None, description="Number of persons benefited."
    )
    percent_vulnerable_marginalized: Optional[float] = Field(
        None, ge=0, le=100,
        description="Percentage of persons benefited from vulnerable and marginalized groups."
    )

class CSRBeneficiaries(BaseModel):
    education: Optional[BeneficiaryGroup] = Field(
        None, description="Beneficiaries in Education."
    )
    employability_and_employment: Optional[BeneficiaryGroup] = Field(
        None, description="Beneficiaries in Employability and Employment."
    )
    entrepreneurship: Optional[BeneficiaryGroup] = Field(
        None, description="Beneficiaries in Entrepreneurship."
    )
    essential_enablers: Optional[BeneficiaryGroup] = Field(
        None, description="Beneficiaries in Essential Enablers."
    )

# __________________________Governance Metrics___________________________________________

class GenderCount(BaseModel):
    male: Optional[int] = Field(None, description="Number of males.")
    female: Optional[int] = Field(None, description="Number of females.")

class DiversityInGovernance(BaseModel):
    board_of_directors: Optional[GenderCount] = Field(
        None, description="Gender breakdown of the board of directors."
    )
    key_management_personnel: Optional[GenderCount] = Field(
        None, description="Gender breakdown of key management personnel."
    )

class NonComplianceInstances(BaseModel):
    board_of_directors: Optional[int] = Field(None, description="Number of complaints against Board of Directors.")
    key_management_personnel: Optional[int] = Field(None, description="Number of complaints against Key Management Personnel.")

class DisciplinaryActionCounts(BaseModel):
    bribery: Optional[int] = Field(
        None,
        description="Number of disciplinary actions taken for bribery."
    )
    corruption: Optional[int] = Field(
        None,
        description="Number of disciplinary actions taken for corruption."
    )

class DisciplinaryActionsTaken(BaseModel):
    directors: Optional[DisciplinaryActionCounts] = Field(
        None,
        description="Disciplinary actions taken against Directors."
    )
    key_management_personnel: Optional[DisciplinaryActionCounts] = Field(
        None,
        description="Disciplinary actions taken against Key Management Personnel."
    )
    employees: Optional[DisciplinaryActionCounts] = Field(
        None,
        description="Disciplinary actions taken against Employees."
    )
    workers: Optional[DisciplinaryActionCounts] = Field(
        None,
        description="Disciplinary actions taken against Workers."
    )

class ConsumerComplaints(BaseModel):
    cyber_security: Optional[int] = Field(
        None,
        description="Number of consumer complaints related to cyber security."
    )
    data_privacy: Optional[int] = Field(
        None,
        description="Number of consumer complaints related to data privacy."
    )
    others: Optional[int] = Field(
        None,
        description="Number of consumer complaints related to other issues."
    )

class CustomerDataBreaches(BaseModel):
    no_pii_involved: Optional[int] = Field(
        None,
        description="Number of customer data breaches where no Personally Identifiable Information (PII) was involved."
    )
    pii_involved: Optional[int] = Field(
        None,
        description="Number of customer data breaches involving Personally Identifiable Information (PII)."
    )

class BusinessOpennessPurchaseConcentration(BaseModel):
    purchase_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Percentage of purchases concentrated with specific suppliers."
    )
    trading_houses_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Percentage of purchases made through trading houses."
    )

class BusinessOpennessSalesConcentration(BaseModel):
    sales_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Percentage of sales concentrated with specific customers or channels."
    )
    dealers_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Percentage of sales made through dealers."
    )

class RelatedPartyTransactionsShare(BaseModel):
    purchase_share_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Share of purchases involving related party transactions (RPT) as a percentage."
    )
    sales_share_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Share of sales involving related party transactions (RPT) as a percentage."
    )


# ------------------------- Environmental -------------------------

class EnvironmentalEmissionsEnergy(BaseModel):
    """Environmental metrics related to emissions and energy consumption."""
    
    emissions: Optional["EmissionDetails"] = Field(
        default=None,
        alias="Emissions",
        description="Breakdown of GHG emissions across Scope 1, 2, and 3. Units in tCO₂e."
    )
    energy_consumption: Optional["EnergyConsumption"] = Field(
        default=None,
        alias="Energy Consumption",
        description="Total energy consumption and intensity metrics in GJ or MWh."
    )


class EnvironmentalWaterWaste(BaseModel):
    """Environmental metrics related to water use and waste management."""
    
    water_withdrawal: Optional["WaterWithdrawalDetails"] = Field(
        default=None,
        alias="Water Withdrawal",
        description="Water withdrawal details and intensity metrics in m³."
    )
    water_discharge: Optional["WaterDischargeDetails"] = Field(
        default=None,
        alias="Water Discharge",
        description="Volume and destination of discharged water, with intensities."
    )
    waste_generation: Optional["WasteGenerationDetails"] = Field(
        default=None,
        alias="Waste Generation",
        description="Total waste generation by category and intensity."
    )
    waste_disposal: Optional["WasteDisposalDetails"] = Field(
        default=None,
        alias="Waste Disposal",
        description="Waste disposal breakdown by method (e.g., landfill, incineration)."
    )
    waste_recovery: Optional["WasteRecoveryDetails"] = Field(
        default=None,
        alias="Waste Recovery",
        description="Recovered or recycled waste details and recovery rate."
    )

# ------------------------- Social -------------------------

class SocialWorkforceAndWellBeing(BaseModel):
    """Social metrics covering workforce composition and well-being initiatives."""
    
    workforce_gender_diversity: Optional["WorkforceGenderDiversity"] = Field(
        default=None,
        alias="Workforce Gender Diversity",
        description="Proportion of employees by gender across the organization."
    )
    turnover_count: Optional["TurnoverCount"] = Field(
        default=None,
        alias="Turnover Count",
        description="Annual employee turnover count or rate."
    )
    employee_well_being_coverage: Optional["EmployeeWellBeingCoverage"] = Field(
        default=None,
        alias="Employee Well-being Coverage",
        description="Programs and initiatives targeting employee well-being."
    )
    worker_well_being_coverage: Optional["WorkerWellBeingCoverage"] = Field(
        default=None,
        alias="Worker Well-being Coverage",
        description="Well-being coverage for contract/temporary workers."
    )
    well_being_cost: Optional["WellBeingCost"] = Field(
        default=None,
        alias="Well-being Cost",
        description="Monetary investment in well-being initiatives."
    )
    wages_by_location: Optional["WagesByLocation"] = Field(
        default=None,
        alias="Wages by Location",
        description="Average wages distributed by geographical location."
    )
    female_wage_share: Optional["FemaleWageShare"] = Field(
        default=None,
        alias="Female Wage Share",
        description="Share of wages received by female employees."
    )


class SocialTrainingAndCSR(BaseModel):
    """Social metrics related to training, safety, and CSR activities."""
    
    human_rights_training_coverage: Optional["HumanRightsTrainingCoverage"] = Field(
        default=None,
        alias="Human Rights Training Coverage",
        description="Percentage of workforce trained on human rights policies."
    )
    health_and_safety_ltifr: Optional["HealthAndSafetyLTIFR"] = Field(
        default=None,
        alias="LTIFR",
        description="Lost Time Injury Frequency Rate (LTIFR) for the reporting period."
    )
    other_health_and_safety_incidents: Optional["OtherHealthAndSafetyIncidents"] = Field(
        default=None,
        alias="Other Safety Incidents",
        description="Other recordable safety incidents beyond LTIFR."
    )
    health_and_safety_training_coverage: Optional["HealthAndSafetyTrainingCoverage"] = Field(
        default=None,
        alias="Health & Safety Training Coverage",
        description="Proportion of employees receiving safety-related training."
    )
    grievances_reported: Optional["GrievancesReported"] = Field(
        default=None,
        alias="Grievances Reported",
        description="Number of employee or stakeholder grievances filed."
    )
    third_party_assessment_coverage_percentage: Optional["ThirdPartyAssessmentCoveragePercentage"] = Field(
        default=None,
        alias="Third-party Assessment Coverage",
        description="Percentage of suppliers or partners assessed by third-party audits."
    )
    csr_beneficiaries: Optional["CSRBeneficiaries"] = Field(
        default=None,
        alias="CSR Beneficiaries",
        description="Individuals or communities positively impacted by CSR programs."
    )

# ------------------------- Governance -------------------------

class GovernanceEthicsAndComplaints(BaseModel):
    """Governance metrics on ethics, compliance, and customer complaints."""
    
    non_compliance_instances: Optional["NonComplianceInstances"] = Field(
        default=None,
        alias="Non-compliance Instances",
        description="Reported legal or regulatory non-compliance cases."
    )
    disciplinary_actions_taken: Optional["DisciplinaryActionsTaken"] = Field(
        default=None,
        alias="Disciplinary Actions",
        description="Actions taken for internal policy breaches."
    )
    consumer_complaints: Optional["ConsumerComplaints"] = Field(
        default=None,
        alias="Consumer Complaints",
        description="Customer complaints received and addressed."
    )
    customer_data_breaches: Optional["CustomerDataBreaches"] = Field(
        default=None,
        alias="Customer Data Breaches",
        description="Incidents involving unauthorized access to customer data."
    )


class GovernanceStructureAndOpenness(BaseModel):
    """Governance metrics related to diversity, structure, and transparency."""
    
    diversity_in_governance: Optional["DiversityInGovernance"] = Field(
        default=None,
        alias="Governance Diversity",
        description="Diversity statistics within governing bodies."
    )
    business_openness_purchase_concentration: Optional["BusinessOpennessPurchaseConcentration"] = Field(
        default=None,
        alias="Purchase Concentration",
        description="Share of purchases concentrated among top suppliers."
    )
    business_openness_sales_concentration: Optional["BusinessOpennessSalesConcentration"] = Field(
        default=None,
        alias="Sales Concentration",
        description="Share of sales concentrated among top customers."
    )
    related_party_transactions_share: Optional["RelatedPartyTransactionsShare"] = Field(
        default=None,
        alias="Related Party Transactions",
        description="Percentage of revenue or cost involving related parties."
    )

class ReportMetadata(BaseModel):
        report_metadata: Optional['ReportDetails'] = Field(
        default=None,
        description="High-level metadata for the ESG report, including reporting year, source, and methodology.",
    )
        
# ___________________Materiality___________________

class ESGMaterialTopicPosition(BaseModel):
    """
    Represents the position of an ESG (Environmental, Social, Governance) material topic 
    on a materiality matrix including its business relevance and stakeholder concern.
    """

    topic_name: str = Field(
        ...,
        description="Name of the ESG material topic (e.g., 'Climate Change', 'Data Privacy').",
        example="Climate Change"
    )

    business_relevance_score: float = Field(
        ...,
        ge=0.0,
        le=5.0,
        description="X-axis score (0-5) representing relevance to the company`s business strategy.",
        example=4.5
    )

    stakeholder_priority_score: float = Field(
        ...,
        ge=0.0,
        le=5.0,
        description="Y-axis score (0-5) indicating stakeholder concern or priority level.",
        example=3.8
    )

    topic_importance_summary: str = Field(
        ...,
        description="Concise summary (2-4 sentences) explaining the topic`s importance and relevance to the organization.",
        example=(
            "Climate change is a critical issue due to its impact on operational resilience, regulatory compliance, "
            "and increasing pressure from investors and customers to adopt sustainable practices."
        )
    )

class Materiality_Metrics(BaseModel):
    material_topics: List['ESGMaterialTopicPosition'] = Field(
        ...,
        description=(
            "List of ESG material topics with coordinates on the materiality matrix, "
            "indicating their importance to both stakeholders and business strategy."
        )
    )