from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_generate_qr():
    response = client.post("/generate-qr/", json={"content": "http://test.com"})
    assert response.status_code == 200
    assert "qr_id" in response.json()
    assert response.json()["status"] == "QR code generated"

def test_fetch_qr():
    # Create a QR code first
    create_resp = client.post("/generate-qr/", json={"content": "http://test.com"})
    qr_id = create_resp.json()["qr_id"]
    
    # Test fetching
    response = client.get(f"/fetch-qr/{qr_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_remove_qr():
    # Create a QR code
    create_resp = client.post("/generate-qr/", json={"content": "http://test.com"})
    qr_id = create_resp.json()["qr_id"]
    
    # Test deletion
    response = client.delete(f"/remove-qr/{qr_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "QR code removed"
    
    # Verify it’s deleted
    response = client.get(f"/fetch-qr/{qr_id}")
    assert response.status_code == 404
