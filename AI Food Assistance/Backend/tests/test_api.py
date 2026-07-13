import sys, os
sys.path.insert(0, os.getcwd())
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_home():
    r = client.get('/')
    assert r.status_code == 200

def test_analytics():
    r = client.get('/analytics/overview')
    assert r.status_code == 200
