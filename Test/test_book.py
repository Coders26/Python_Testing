from flask.testing import FlaskClient
import pytest
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)

    # Renvoie des valeurs fictives pour les listes clubs et competitions
    clubs = [{'name': 'ClubA'}, {'name': 'ClubB'}]
    competitions = [{'name': 'CompetitionA'}, {'name': 'CompetitionB'}]

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club]
        foundCompetition = [c for c in competitions if c['name'] == competition]
        if foundClub and foundCompetition:
            return "Booking page"
        else:
            return "Something went wrong"

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_book_valid(client: FlaskClient):
    response = client.get('/book/CompetitionA/ClubA')
    assert response.status_code == 200
    assert b"Booking page" in response.data

def test_book_invalid(client: FlaskClient):
    response = client.get('/book/CompetitionC/ClubB')
    assert response.status_code == 200
    assert b"Something went wrong" in response.data

def test_book_invalid_club(client: FlaskClient):
    response = client.get('/book/CompetitionA/ClubC')
    assert response.status_code == 200
    assert b"Something went wrong" in response.data

def test_book_invalid_competition(client: FlaskClient):
    response = client.get('/book/CompetitionC/ClubA')
    assert response.status_code == 200
    assert b"Something went wrong" in response.data

def test_book_missing_parameters(client: FlaskClient):
    response = client.get('/book/')
    assert response.status_code == 404

    response = client.get('/book/CompetitionA/')
    assert response.status_code == 404

    response = client.get('/book//ClubA')
    assert response.status_code == 404