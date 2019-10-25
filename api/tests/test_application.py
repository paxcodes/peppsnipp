from application import create_app
from flask import session

def test_appLoadsConfig():
  app = create_app()
  assert app.config['FLASK_APP'] == "application"

def test_session():
  app = create_app()
  with app.test_client() as client:
    client.get('/dropbox')
    assert session['message'] == 'Hello World!'
