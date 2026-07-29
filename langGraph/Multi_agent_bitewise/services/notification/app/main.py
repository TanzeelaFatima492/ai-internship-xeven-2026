﻿from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import uvicorn
import os
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title='BiteWise Notification Service',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ==================== IN-MEMORY STORE ====================
notifications_db: Dict[str, list] = {}  # user_id -> list of notifications
active_connections: Dict[str, WebSocket] = {}

# ==================== MODELS ====================
class NotifyRequest(BaseModel):
    user_id: str
    message: str
    type: str = "info"
    offer: Optional[dict] = None
    channels: Optional[List[str]] = ["in_app"]

class NotificationResponse(BaseModel):
    notifications: List[dict]
    total: int
    unread: int

# ==================== WEBSOCKET ====================
@app.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    try:
        await websocket.accept()
        active_connections[user_id] = websocket
        
        # Send existing notifications on connect
        user_notifs = notifications_db.get(user_id, [])
        await websocket.send_text(json.dumps({
            "type": "existing_notifications",
            "data": user_notifs
        }))
        
        print(f'Connected: {user_id}')
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if user_id in active_connections:
            del active_connections[user_id]
        print(f'Disconnected: {user_id}')

# ==================== REST ENDPOINTS ====================

@app.get('/notifications/{user_id}')
async def get_notifications(user_id: str, limit: int = 50):
    """Get notifications for a user"""
    user_notifs = notifications_db.get(user_id, [])
    limited = user_notifs[-limit:] if len(user_notifs) > limit else user_notifs
    unread = sum(1 for n in user_notifs if not n.get("read", False))
    
    return {
        "notifications": limited,
        "total": len(user_notifs),
        "unread": unread
    }

@app.put('/notifications/{user_id}/{notification_id}/read')
async def mark_notification_read(user_id: str, notification_id: str):
    """Mark a single notification as read"""
    user_notifs = notifications_db.get(user_id, [])
    for notif in user_notifs:
        if notif["id"] == notification_id:
            notif["read"] = True
            return {"success": True, "message": "Marked as read"}
    raise HTTPException(status_code=404, detail="Notification not found")

@app.put('/notifications/{user_id}/read-all')
async def mark_all_read(user_id: str):
    """Mark all notifications as read for a user"""
    user_notifs = notifications_db.get(user_id, [])
    for notif in user_notifs:
        notif["read"] = True
    return {"success": True, "message": "All marked as read"}

@app.delete('/notifications/{user_id}/{notification_id}')
async def delete_notification(user_id: str, notification_id: str):
    """Delete a single notification"""
    user_notifs = notifications_db.get(user_id, [])
    filtered = [n for n in user_notifs if n["id"] != notification_id]
    if len(filtered) == len(user_notifs):
        raise HTTPException(status_code=404, detail="Notification not found")
    notifications_db[user_id] = filtered
    return {"success": True, "message": "Deleted"}

@app.post('/notify')
async def send_notification(request: NotifyRequest):
    """Send a notification to a user (REST + WebSocket broadcast)"""
    notification = {
        "id": str(uuid.uuid4()),
        "user_id": request.user_id,
        "message": request.message,
        "type": request.type,
        "offer": request.offer or {},
        "read": False,
        "created_at": datetime.utcnow().isoformat(),
        "icon": "🔔"
    }
    
    # Store in database
    if request.user_id not in notifications_db:
        notifications_db[request.user_id] = []
    notifications_db[request.user_id].append(notification)
    
    # Send via WebSocket if connected
    ws = active_connections.get(request.user_id)
    if ws:
        try:
            await ws.send_text(json.dumps({
                "type": "new_notification",
                "data": notification
            }))
        except:
            pass
    
    return {
        "success": True,
        "notification_id": notification["id"],
        "message": "Notification sent"
    }

@app.get('/health')
async def health():
    return {'status': 'healthy', 'total_notifications': sum(len(v) for v in notifications_db.values())}

@app.get('/')
async def root():
    return {
        'service': 'Notification',
        'connections': len(active_connections),
        'total_notifications': sum(len(v) for v in notifications_db.values())
    }

if __name__ == '__main__':
    port = int(os.getenv('NOTIFICATION_SERVICE_PORT', 8003))
    uvicorn.run(app, host='127.0.0.1', port=port)
