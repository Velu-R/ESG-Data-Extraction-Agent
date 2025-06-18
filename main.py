# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from src.backend.api.routes import router as api_router

# app = FastAPI(
#     title="Sustainability Report Extractor API",
#     description="An API for extracting sustainability metadata using a LangChain-based supervisor agent.",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(api_router)

import os

EXCLUDE_DIRS = {'.git', '.venv', '.pytest_cache', '__pycache__', '.langgraph_api'}

def print_tree(start_path='.', prefix='', max_depth=5, current_depth=0):
    if current_depth > max_depth or not os.path.exists(start_path):
        return

    entries = sorted([
        e for e in os.listdir(start_path)
        if e not in EXCLUDE_DIRS
    ])

    for index, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension, max_depth, current_depth + 1)

if __name__ == "__main__":
    print("📁 Project Tree:")
    print_tree()
