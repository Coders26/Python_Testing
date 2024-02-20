import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_show_summary_valid_client(client):
    # Simulate a valid POST request with the correct email
    response = client.post('/showSummary', data={'email': 'john@simplylift.com'})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 302

    # Add more assertions based on the expected behavior of your function
    # For example, you can check if certain content is present in the response HTML.


def test_show_summary_invalid_client(client):
    # Simulez une requête avec un email invalide
    response = client.post('/showSummary', data={'email': 'nonexistent@example.com'})

    # Assurez-vous que le statut de la réponse est 302 (redirection vers la page d'accueil)
    assert response.status_code == 302

    # Assurez-vous que l'URL de redirection se termine par "/"
    assert response.headers['Location'].endswith('/')


    # Add more assertions if needed

# You can add more test cases to cover different scenarios
def test_show_summary_no_email(client):
    # Simulez une requête sans email
    response = client.post('/showSummary', data={})

    # Assurez-vous que le statut de la réponse est 302 (redirection vers la page d'accueil)
    assert response.status_code == 302

    # Assurez-vous que l'URL de redirection se termine par "/"
    assert response.headers['Location'].endswith('/')

    # Vérifiez si un message d'erreur approprié est présent dans les messages flash
    with client.session_transaction() as session:
        flash_messages = dict(session['_flashes'])
        assert 'Veuillez entrer votre adresse mail!' in flash_messages['error']


def test_show_summary_multiple_matching_clubs(client):
    # Ajoutez plusieurs clubs avec la même adresse e-mail
    app.config['clubs'] = [
        {"name": "Club 1", "email": "john@simplylift.com", "points": 13},
        {"name": "Club 2", "email": "john@simplylift.com", "points": 10},
    ]

    # Simulez une requête avec une adresse e-mail qui correspond à plusieurs clubs
    response = client.post('/showSummary', data={'email': 'john@simplylift.com'})

    # Assurez-vous que le statut de la réponse est 302 (redirection)
    assert response.status_code == 302

    # Assurez-vous que l'URL de redirection se termine par "/"
    assert response.headers['Location'].endswith('/')

    # Vérifiez si un message d'erreur approprié est présent dans les messages flash
    with client.session_transaction() as session:
        flash_messages = dict(session['_flashes'])
