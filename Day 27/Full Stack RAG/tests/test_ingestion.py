import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.rag.ingestion_service import IngestionService

service = IngestionService()

print("IngestionService initialized successfully!")