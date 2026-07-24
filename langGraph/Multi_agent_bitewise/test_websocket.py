import asyncio
import websockets
import json
import requests

# ==================== CONFIGURATION ====================
NOTIFICATION_URL = "http://localhost:8003"
WS_URL = "ws://localhost:8003/ws/user-001"
USER_ID = "user-001"

# ==================== FUNCTIONS ====================

async def listen_for_notifications():
    """Listen for real-time notifications via WebSocket"""
    print(f"🔌 Connecting to WebSocket for user: {USER_ID}")
    print("=" * 50)
    
    try:
        async with websockets.connect(WS_URL) as websocket:
            print(f"✅ Connected to WebSocket!")
            print("📡 Waiting for real-time notifications...")
            print("=" * 50)
            
            while True:
                try:
                    # Receive message
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    # Handle different message types
                    if data.get("type") == "existing_notifications":
                        print("\n📬 Existing Notifications:")
                        notifications = data.get("data", [])
                        for notif in notifications:
                            print(f"   🔔 {notif['message']}")
                        print("=" * 50)
                    
                    elif data.get("type") == "new_notification":
                        print("\n🔴 NEW NOTIFICATION RECEIVED!")
                        notification = data.get("data", {})
                        print(f"   📩 Message: {notification['message']}")
                        print(f"   🎯 Type: {notification.get('type', 'unknown')}")
                        print(f"   ⭐ Priority: {notification.get('priority', 'low')}")
                        
                        # Auto-mark as read
                        if notification.get("id"):
                            try:
                                response = requests.put(
                                    f"{NOTIFICATION_URL}/notifications/{USER_ID}/{notification['id']}/read"
                                )
                                if response.status_code == 200:
                                    print("   ✅ Auto-marked as read")
                            except:
                                pass
                        print("=" * 50)
                    
                except websockets.exceptions.ConnectionClosed:
                    print("\n⚠️ Connection closed. Reconnecting...")
                    break
                except json.JSONDecodeError:
                    print(f"\n⚠️ Invalid JSON received: {message}")
                except Exception as e:
                    print(f"\n⚠️ Error: {e}")
                    
    except Exception as e:
        print(f"\n❌ Failed to connect: {e}")

async def trigger_notification():
    """Trigger a notification to test WebSocket"""
    print("\n🚀 Triggering test notification...")
    
    try:
        response = requests.post(
            f"{NOTIFICATION_URL}/notify",
            json={
                "user_id": USER_ID,
                "offer": {
                    "type": "test_notification",
                    "message": "🔄 This is a WebSocket test notification!",
                    "priority": "high",
                    "discount": "20% off"
                },
                "channels": ["in_app"]
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Notification sent! ID: {result.get('notification_id')}")
        else:
            print(f"❌ Failed to send: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== MAIN ====================

async def main():
    print("=" * 60)
    print("        BiteWise WebSocket Notification Test")
    print("=" * 60)
    
    # Start listener and trigger notification
    listener_task = asyncio.create_task(listen_for_notifications())
    
    # Wait a bit for connection
    await asyncio.sleep(2)
    
    # Trigger notification
    await trigger_notification()
    
    # Wait for notifications
    await asyncio.sleep(10)
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(main())