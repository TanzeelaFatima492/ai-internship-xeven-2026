from fastapi import FastAPI
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="BiteWise Smart Offers Service",
    version="1.0.0",
    description="Generates personalized offers for users"
)

@app.get("/")
async def root():
    return {
        "service": "Smart Offers Service",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("SMART_OFFERS_SERVICE_PORT", 8002))
    uvicorn.run(app, host="127.0.0.1", port=port)