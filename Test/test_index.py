import pytest
from datetime import datetime
from app import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    competitions = loadCompetitions(datetime.strptime("2024-02-12 09:00:00", "%Y-%m-%d %H:%M:%S"))
    clubs = loadClubs()
    # Envoyer une demande GET à la route index
    response = client.get('/')
    # Vérification que le code de statut de la réponse est 200 (OK)
    assert response.status_code == 200
    # Vérification que la réponse contient les noms des compétitions et des clubs
    for competition in competitions:
        assert competition['name'] in response.data.decode('utf-8')
        assert str(competition['numberOfPlaces']) in response.data.decode('utf-8')
    for club in clubs:
        assert club['name'] in response.data.decode('utf-8')
        assert club['email'] in response.data.decode('utf-8')
        assert str(club['points']) in response.data.decode('utf-8')