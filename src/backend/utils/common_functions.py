import re

def is_valid_metadata(data: dict) -> bool:
    """
    Check if metadata contains all required fields.
    """
    required_fields = {"company_name", "sector", "industry", "headquarters", "country", "region"}
    valid = isinstance(data, dict) and required_fields.issubset(data.keys())
    return valid

def clean_json_output(raw_output: str) -> str:
    """
    Remove markdown/code fences and return plain JSON string.
    """
    cleaned = re.sub(r"```(?:json)?", "", raw_output).strip("` \n")
    return cleaned
