import sys
from pathlib import Path

print("TEST FILE STARTED")

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.rag.index_manager import IndexManager

print("IMPORT SUCCESS")

manager = IndexManager()

print("OBJECT CREATED")