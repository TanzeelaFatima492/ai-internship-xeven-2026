import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

# ==================== PUSH NOTIFICATION ====================

def send_push_notification(user_id: str, title: str, body: str, data: Dict = None) -> bool:
    """
    Send push notification via Firebase Cloud Messaging (FCM)
    """
    try:
        # FCM API call (mock)
        print(f"📱 Sending push to {user_id}: {title} - {body}")
        # In production:
        # response = requests.post(
        #     "https://fcm.googleapis.com/v1/projects/your-project/messages:send",
        #     headers={"Authorization": f"Bearer {FCM_KEY}"},
        #     json={"message": {...}}
        # )
        return True
    except Exception as e:
        print(f"Push notification failed: {e}")
        return False

# ==================== EMAIL NOTIFICATION ====================

def send_email_notification(email: str, subject: str, body: str) -> bool:
    """
    Send email notification via SendGrid/SMTP
    """
    try:
        print(f"📧 Sending email to {email}: {subject}")
        # In production:
        # response = requests.post(
        #     "https://api.sendgrid.com/v3/mail/send",
        #     headers={"Authorization": f"Bearer {SENDGRID_KEY}"},
        #     json={"personalizations": [...], "content": [...]}
        # )
        return True
    except Exception as e:
        print(f"Email notification failed: {e}")
        return False

# ==================== SMS NOTIFICATION ====================

def send_sms_notification(phone: str, message: str) -> bool:
    """
    Send SMS via Twilio
    """
    try:
        print(f"📱 Sending SMS to {phone}: {message[:50]}...")
        # In production:
        # response = requests.post(
        #     "https://api.twilio.com/2010-04-01/Accounts/.../Messages.json",
        #     auth=(ACCOUNT_SID, AUTH_TOKEN),
        #     data={"To": phone, "From": TWILIO_NUMBER, "Body": message}
        # )
        return True
    except Exception as e:
        print(f"SMS notification failed: {e}")
        return False

# ==================== NOTIFICATION FORMATTER ====================

def format_notification_message(notification_type: str, data: Dict) -> str:
    """
    Format notification message based on type
    """
    templates = {
        "order_confirmation": "✅ Order #{order_id} confirmed! Total: ${total}",
        "order_delivered": "🚚 Order #{order_id} delivered! Enjoy your meal!",
        "offer_available": "🎉 New offer available: {offer_name} - {discount}",
        "streak_warning": "🔥 Don't break your {streak}-day streak!",
    }
    
    template = templates.get(notification_type, "{message}")
    try:
        return template.format(**data)
    except:
        return template.replace("{", "").replace("}", "")

# ==================== NOTIFICATION FILTER ====================

def filter_notifications(notifications: List[Dict], filters: Dict) -> List[Dict]:
    """
    Filter notifications by type, read status, date range
    """
    filtered = notifications
    
    if filters.get("type"):
        filtered = [n for n in filtered if n.get("type") == filters["type"]]
    
    if filters.get("read") is not None:
        filtered = [n for n in filtered if n.get("read") == filters["read"]]
    
    if filters.get("start_date"):
        start = datetime.fromisoformat(filters["start_date"])
        filtered = [n for n in filtered if datetime.fromisoformat(n["created_at"]) >= start]
    
    if filters.get("end_date"):
        end = datetime.fromisoformat(filters["end_date"])
        filtered = [n for n in filtered if datetime.fromisoformat(n["created_at"]) <= end]
    
    return filtered

# ==================== NOTIFICATION STATS ====================

def get_notification_stats(notifications: List[Dict]) -> Dict:
    """
    Get statistics about notifications
    """
    total = len(notifications)
    unread = sum(1 for n in notifications if not n.get("read", False))
    read = total - unread
    
    # Count by type
    type_counts = {}
    for n in notifications:
        n_type = n.get("type", "unknown")
        type_counts[n_type] = type_counts.get(n_type, 0) + 1
    
    return {
        "total": total,
        "read": read,
        "unread": unread,
        "read_rate": round(read / total * 100, 2) if total > 0 else 0,
        "by_type": type_counts
    }