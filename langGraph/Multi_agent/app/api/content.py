from fastapi import APIRouter
from app.agents.supervisor_agent import SupervisorAgent

router = APIRouter()
supervisor = None

@router.on_event("startup")
async def init():
    global supervisor
    supervisor = await SupervisorAgent().initialize()
    print("✅ Multi-Agent Content Studio Ready!")

@router.post("/generate-content")
async def generate_content(topic: str):
    try:
        result = await supervisor.create_content(topic)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}