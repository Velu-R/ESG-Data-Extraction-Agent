import os
import re
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure, PyMongoError
from pymongo.collection import Collection
from datetime import datetime
from unidecode import unidecode
from pymongo import MongoClient, errors
from bson import ObjectId

from src.backend.utils.logger import get_logger

logger = get_logger()
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]
ESG_REPORT_EXTRACTS_COLLECTION = "esg_report_extracts"
# ESG_REPORT_EXTRACTS = "esg_report_extracts"



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

def get_mongo_client() -> Optional[MongoClient]:
    """
    Establishes and returns a MongoDB client using credentials from the environment.
    """
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        return client
    except ConnectionFailure:
        logger.error("MongoDB connection failed. Please check MONGODB_URI.")
    except Exception as e:
        logger.exception(f"Unexpected error while connecting to MongoDB: {str(e)}")
    return None

def store_document(collection_name: str, document: Dict) -> Optional[str]:
    """
    Stores a document in MongoDB if it doesn't already exist.

    Args:
        collection_name (str): Name of the MongoDB collection.
        document (Dict): The document to be inserted.

    Returns:
        Optional[str]: Inserted document ID if successful, None otherwise.
    """
    try:
        client = get_mongo_client()
        if client is None:
            logger.error("MongoDB client is not available.")
            return None
        
        sanitized_collection_name = sanitize_collection_name(collection_name)
        db = client.get_database(MONGODB_DB_NAME)
        collection = db[sanitized_collection_name]

        # Check if a similar document already exists
        existing_document = collection.find_one(document)
        if existing_document:
            logger.info(f"Document already exists with ID: {existing_document['_id']}")
            return str(existing_document['_id'])

        # If no existing document, insert the new one
        result = collection.insert_one(document)
        logger.info(f"New document inserted with ID: {result.inserted_id}")
        return str(result.inserted_id)

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
    
    return None

def upsert_document(collection_name: str, filter_fields: dict, document: dict) -> None:
    """
    Upsert a document into MongoDB collection based on a filter_fields.

    Args:
        collection_name (str): The target collection.
        filter_fields (dict): The filter to find the existing document.
        document (dict): The new data to insert or update.
    """
    try:
        collection: Collection = db[collection_name]
        document["ingested_at"] = datetime.now()
        result = collection.update_one(
            filter=filter_fields,
            update={"$set": document},
            upsert=True
        )
        if result.matched_count:
            logger.info(f"Updated document in '{collection_name}' with query {filter_fields}")
        else:
            logger.info(f"Inserted new document in '{collection_name}' with query {filter_fields}")
    except Exception as e:
        logger.error(f"Failed to upsert document in '{collection_name}' with query {filter_fields}: {e}")
        raise

# def upsert_document(collection_name: str, document: Dict, filter: Optional[Dict] = None) -> Optional[str]:
#     """
#     Inserts or updates a document in MongoDB based on a unique filter.

#     Args:
#         collection_name (str): MongoDB collection name.
#         document (Dict): The document to insert or update.
#         filter (Optional[Dict]): Unique fields to identify the document.

#     Returns:
#         Optional[str]: Document ID (existing or inserted), or None on failure.
#     """
#     try:
#         client = get_mongo_client()
#         if client is None:
#             logger.error("MongoDB client unavailable.")
#             return None

#         sanitized_collection_name = sanitize_collection_name(collection_name)
#         db = client.get_database(DB_NAME)
#         collection = db[sanitized_collection_name]

#         # Ensure filter is valid
#         if not filter or not isinstance(filter, dict):
#             logger.warning("Invalid or missing filter for upsert. Using full document as filter.")
#             filter = document

#         result = collection.update_one(
#             filter=filter,
#             update={"$set": document},
#             upsert=True
#         )

#         if result.upserted_id:
#             logger.info(f"Inserted new document with ID: {result.upserted_id}")
#             return str(result.upserted_id)
#         else:
#             existing = collection.find_one(filter)
#             if existing:
#                 logger.info(f"Updated existing document with ID: {existing['_id']}")
#                 return str(existing['_id'])
#             else:
#                 logger.warning("No matching document found after update.")
#                 return None

#     except Exception as e:
#         logger.exception(f"MongoDB upsert failed: {str(e)}")
#         return None

# def retrieve_documents(collection_name: str, query: Optional[Dict] = None) -> List[Dict]:
#     """
#     Retrieves documents from the specified MongoDB collection.

#     Args:
#         collection_name (str): Name of the MongoDB collection.
#         query (Optional[Dict]): A MongoDB query filter. Defaults to {} (fetch all documents).

#     Returns:
#         List[Dict]: A list of documents matching the query. Empty list if none found or error occurs.
#     """
#     try:
#         client = get_mongo_client()
#         if client is None:
#             logger.error("MongoDB client is not available.")
#             return []

#         db = client.get_database(MONGODB_DB_NAME)
#         collection = db[collection_name]

#         documents_cursor = collection.find(query or {})
#         documents = list(documents_cursor)

#         logger.info(f"Retrieved {len(documents)} documents from collection: {collection_name}")
#         return documents

#     except Exception as e:
#         logger.exception(f"An error occurred while retrieving documents: {str(e)}")
#         return []

def retrieve_documents(
    collection_name: str,
    query: Optional[Dict] = None,
    only_ids: bool = False,
    single: bool = False,
    company_legal_name: Optional[str] = None,
    reporting_year: Optional[int] = None
) -> Union[List[Dict], Dict, None]:
    """
    Retrieves documents from a specified MongoDB collection with optional filtering.

    Args:
        collection_name (str): MongoDB collection name.
        query (Optional[Dict]): MongoDB query filter.
        only_ids (bool): If True, return only _id field for all documents.
        single (bool): If True, return only a single matching document.
        company_legal_name (Optional[str]): Filter by company_legal_name.
        reporting_year (Optional[int]): Filter by reporting_year inside 'esg_report'.

    Returns:
        Union[List[Dict], Dict, None]: A list of documents, a single document, or None.
    """
    try:
        client = get_mongo_client()
        if client is None:
            logger.error("MongoDB client is not available.")
            return [] if not single else None

        db = client[MONGODB_DB_NAME]
        collection = db[collection_name]

        mongo_query = query or {}

        # Build query from parameters if provided
        if company_legal_name:
            mongo_query["report_metadata.company_legal_name"] = company_legal_name
        if reporting_year is not None:
            mongo_query["esg_report.year"] = reporting_year

        projection = {"_id": 1} if only_ids else None

        if single:
            result = collection.find_one(mongo_query, projection)
            logger.info(f"Retrieved single document from {collection_name} for query: {mongo_query}")
            return result

        documents_cursor = collection.find(mongo_query, projection)
        documents = list(documents_cursor)
        logger.info(f"Retrieved {len(documents)} documents from collection: {collection_name}")
        return documents

    except Exception as e:
        logger.exception(f"An error occurred while retrieving documents: {str(e)}")
        return [] if not single else None

    
def list_collections() -> List[str]:
    """
    Lists all collections in the MongoDB database.
    
    Returns:
        List[str]: A list of collection names in the database.
    """
    try:
        client = get_mongo_client()
        if client is None:
            return []

        db = client[MONGODB_DB_NAME]
        collections = db.list_collection_names()
        logger.info(f"Found {len(collections)} collections in '{MONGODB_DB_NAME}'")
        return collections

    except PyMongoError as e:
        logger.exception(f"Failed to list collections: {str(e)}")
    except Exception as e:
        logger.exception(f"Unexpected error while listing collections: {str(e)}")
    return []

# def upsert_esg_report(document: dict, collection_name: str):
#     """
#     Upserts a year-specific ESG report into the 'esg_reports' array for the given company (_id).
#     If the report for the year exists, it is updated. Otherwise, it is appended.

#     Args:
#         document (dict): Must contain:
#                          - '_id': str (company identifier)
#                          - 'reporting_year': int
#                          - 'esg_report': dict (actual ESG data)
#         collection_name (str): MongoDB collection name.

#     Raises:
#         ValueError: If required fields are missing or invalid.
#         PyMongoError: On MongoDB operation failure.
#     """
#     required_fields = ["_id", "reporting_year", "esg_report"]
#     missing = [f for f in required_fields if f not in document]
#     if missing:
#         raise ValueError(f"Missing required fields: {', '.join(missing)}")

#     company_id = document["_id"]
#     reporting_year = document["reporting_year"]
#     esg_data = document["esg_report"]

#     if not isinstance(company_id, str):
#         raise ValueError("'_id' must be a string.")
#     if not isinstance(reporting_year, int):
#         raise ValueError("'reporting_year' must be an integer.")
#     if not isinstance(esg_data, dict):
#         raise ValueError("'esg_report' must be a dictionary.")

#     timestamp = datetime.now()
#     esg_data["year"] = reporting_year
#     esg_data["updated_at"] = timestamp

#     try:
#         with get_mongo_client() as client:
#             db = client[MONGODB_DB_NAME]
#             collection = db[collection_name]

#             # Attempt to update existing ESG report for the year
#             result = collection.update_one(
#                 {
#                     "_id": company_id,
#                     "esg_reports.year": reporting_year
#                 },
#                 {
#                     "$set": {
#                         "esg_reports.$": esg_data
#                     }
#                 }
#             )

#             if result.matched_count == 0:
#                 # Insert new ESG report for the year
#                 esg_data["created_at"] = timestamp
#                 collection.update_one(
#                     {"_id": company_id},
#                     {
#                         "$push": {"esg_reports": esg_data},
#                         "$setOnInsert": {"_id": company_id}
#                     },
#                     upsert=True
#                 )
#                 logger.info(f"[ESG] Inserted new report for '{company_id}' ({reporting_year}).")
#             else:
#                 logger.info(f"[ESG] Updated report for '{company_id}' ({reporting_year}).")

#     except PyMongoError as e:
#         logger.error(f"[ESG] Upsert failed for '{company_id}' ({reporting_year}): {str(e)}")
#         raise

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
        collection = db[ESG_REPORT_EXTRACTS_COLLECTION]

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
        collection = db[collection_name]

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