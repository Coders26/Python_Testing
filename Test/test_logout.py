import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_logout_redirects_to_index(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200