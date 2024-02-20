import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
import pytest
from flask import Flask, render_template, request, flash, get_flashed_messages
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchasePlaces(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '25'
    }
    competitions = [{"name": "Spring Festival", "numberOfPlaces": 100}]  # Replace with your test data
    clubs = [{"name": "Iron Temple", "points": 50}]  # Replace with your test data
    response = client.post('/purchasePlaces', data=data)
    competition_name = data['competition']
    club_name = data['club']
    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)
    with client.session_transaction() as session:
        flashed_messages = get_flashed_messages()
        print(flashed_messages)