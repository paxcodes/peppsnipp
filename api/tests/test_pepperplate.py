import pytest
from os import getenv

from application import create_app
from tests import saveResponse


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def testPepperplateLogin(client):
    postData = {
        "email": getenv("PEPPERPLATE_EMAIL"),
        "password": getenv("PEPPERPLATE_PW")
    }
    response = client.post('/pepperplate/session', data=postData)
    saveResponse(response, resource="peppSession")
    assert 'Rosalyn' == response.json['usersName']
    assert 315 == response.json['recipeTotal']
