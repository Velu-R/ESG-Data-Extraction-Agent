from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.api.routes import router as api_router

app = FastAPI(
    title="Sustainability Report Extractor API",
    description="An API for extracting sustainability metadata using a LangChain-based supervisor agent.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)