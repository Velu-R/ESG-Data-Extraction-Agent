import re
from typing import List, Dict
from dotenv import load_dotenv
from pymongo.errors import PyMongoError
from unidecode import unidecode
from pymongo import errors
from bson import ObjectId

from src.backend.utils.logger import get_logger
from src.backend.config.config import config

logger = get_logger()
load_dotenv()

def sanitize_collection_name(name: str) -> str:
    """
    Removes trailing special characters not allowed in MongoDB collection names.
    MongoDB restrictions:
      - Cannot contain null characters (\0)
      - Cannot start with "system."
      - Cannot contain "$"
      - Avoid ending in "." or " " (space)
    """
    name = re.sub(r'[\0$]', '', name)
    name = re.sub(r'[.\s]+$', '', name)
    if name.startswith("system."):
        name = name.replace("system.", "system_")
    return name

def slugify_company(name: str) -> str:
    return unidecode(name.strip().lower().replace(" ", "_"))

def list_collections() -> List[str]:
    """
    Lists all collections in the MongoDB database.
    
    Returns:
        List[str]: A list of collection names in the database.
    """
    try:
        db = config.mongo_db
        collections = db.list_collection_names()
        logger.info(f"Found {len(collections)} collections in '{db}'")
        return collections

    except PyMongoError as e:
        logger.exception(f"Failed to list collections: {str(e)}")
    except Exception as e:
        logger.exception(f"Unexpected error while listing collections: {str(e)}")
    return []

def upsert_esg_report(document: Dict) -> bool:
    """
    Upserts a year-specific ESG report into the 'esg_reports.{year}' field of a company document.

    If the company (_id) exists, the ESG report for the given year is updated. Otherwise,
    a new document is created. Logs success or error.

    Args:
        document (Dict): Must contain '_id', 'year', and 'esg_report'.

    Returns:
        Dict[str, Any]: Result including status ('inserted' or 'updated'), message, and identifiers.
    """
    try:
        logger.info(f"Document : {document}")
        required_keys = {"_id", "year", "esg_report"}
        if not required_keys.issubset(document):
            missing = required_keys - document.keys()
            msg = f"Missing keys in document: {missing}"
            logger.error(msg)
            return {"status": "error", "message": msg}

        company_id = document["_id"]
        year = str(document["year"])
        esg_report_data = document["esg_report"]

        update_path = f"esg_reports.{year}"
        update_doc = { "$set": { update_path: esg_report_data }}
        collection = config.ESG_REPORT_COLLECTION

        result = collection.update_one(
            { "_id": company_id },
            update_doc,
            upsert=True
        )

        if result.upserted_id:
            msg = f"ESG report inserted for company_id={company_id}, year={year}"
            logger.info(msg)
            return {
                "status": "inserted",
                "company_id": company_id,
                "year": year,
                "message": msg
            }
        
        elif result.modified_count > 0:
            msg = f"ESG report updated for company_id={company_id}, year={year}"
            logger.info(msg)
            return {
                "status": "updated",
                "company_id": company_id,
                "year": year,
                "message": msg
            }
        
        else:
            msg = f"No changes made to ESG report for company_id={company_id}, year={year}"
            logger.info(msg)
            return {
                "status": "unchanged",
                "company_id": company_id,
                "year": year,
                "message": msg
            }
    except Exception as e:
        msg = f"Exception during ESG report upsert: {e}"
        logger.error(msg)
        return {
            "status": "error",
            "company_id": document.get("_id"),
            "year": str(document.get("year", "")),
            "message": msg
        }

def retrieve_document_by_id(collection_name: str, document_id, convert_to_object_id: bool = False):
    """
    Retrieve a single document from a MongoDB collection by _id.

    Args:
        collection_name (str): The name of the MongoDB collection.
        document_id (str or ObjectId): The value of the _id to retrieve.
        convert_to_object_id (bool): Set to True if _id is an ObjectId, not a string.

    Returns:
        dict or None: The document if found, otherwise None.

    Raises:
        ValueError: If inputs are invalid.
        Exception: For any unexpected database errors.
    """
    if not collection_name or not isinstance(collection_name, str):
        raise ValueError("Invalid collection name.")

    if document_id is None:
        raise ValueError("document_id must not be None.")

    try:
        collection = config.ESG_REPORT_COLLECTION

        if convert_to_object_id:
            try:
                document_id = ObjectId(document_id)
            except Exception as e:
                raise ValueError(f"Invalid ObjectId format: {document_id}") from e

        document = collection.find_one({"_id": document_id})

        if document:
            logger.info(f"Document found with _id: {document_id}")
            return document
        else:
            logger.error(f"No document found with _id: {document_id}")
            return None

    except errors.PyMongoError as e:
        logger.error(f"Database error while retrieving document: {e}")
        raise

    except Exception as ex:
        logger.error(f"Unexpected error: {ex}")
        raise

# all_docs = retrieve_documents(collection_name=ESG_REPORT_EXTRACTS_COLLECTION)
# print(all_docs[0]["_id"])

# collection = list_collections()
# print(collection)