import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
import pytest
from app import loadClubs
from flask import Flask
from app import app
import sys
from pathlib import Path


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchasePlaces_valid_reservation(client):
    response = client.post('/purchasePlaces',
                           data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '13'},
                           follow_redirects=True)
    assert response.status_code == 200


# Test purchasePlaces route for edge cases
# Test purchasePlaces route for edge cases
def test_purchasePlaces_edge_cases(client):
    # Charger les données des clubs depuis le fichier JSON ou initialiser directement
    clubs = loadClubs()

    # Test case where number of places equals 12
    response = client.post('/purchasePlaces',
                           data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '12'},
                           follow_redirects=True)
    assert response.status_code == 200

    # Test case where club has just enough points
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    club['points'] = 13
    response = client.post('/purchasePlaces',
                           data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '13'},
                           follow_redirects=True)
    assert response.status_code == 200

    # Test case where club has more than enough points
    club['points'] = 20
    response = client.post('/purchasePlaces',
                           data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '13'},
                           follow_redirects=True)
    assert response.status_code == 200