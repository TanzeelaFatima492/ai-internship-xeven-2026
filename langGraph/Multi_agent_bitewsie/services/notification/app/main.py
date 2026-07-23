from fastapi import FastAPI
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="BiteWise Notification Service",
    version="1.0.0",
    description="Sends real-time notifications to users"
)

@app.get("/")
async def root():
    return {
        "service": "Notification Service",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("NOTIFICATION_SERVICE_PORT", 8004))
    uvicorn.run(app, host="127.0.0.1", port=port)