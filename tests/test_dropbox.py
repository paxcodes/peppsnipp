from dropbox.oauth import OAuth2FlowResult, DropboxOAuth2Flow
from application import create_app
from urllib.parse import urlparse
from flask import session

import pytest

@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  with app.test_client() as client:
    yield client
  
def test_dropbox_oauth_start(client):
  response = client.get('/dropbox/start')
  
  expectedNetworkLocation = "www.dropbox.com"
  assert response.status_code == 302
  assert urlparse(response.location).netloc == expectedNetworkLocation

def test_dropbox_oauth_finish(client, monkeypatch):
  query_string = {
    'state': 'sojhqf2nGunEIxI-MdePeg%3D%3D',
    'code': 'pQbO_7SMV2AAAAAAAAAAL_Tpd0uws8RpRTO2OBQAXwI'
  }
  
  oauth2flow_result = OAuth2FlowResult(
    'pQbO_7SMV2AAAAAAAAAANBT3CBXzAA9lq_dYbBRhkBu_FGcnV4MqaRziQQVqs6Rr',
    'dbid:AADcI8OF_48Hgl7UEQEFuJAll68DWhjvREU', 
    '2233275040', 
    None
  )
  
  with client.session_transaction() as sess:
      sess['dropbox-auth-csrf-token'] = query_string['state']
    
  def mock_dropbox_finish(*args):
    return oauth2flow_result
    
  monkeypatch.setattr(DropboxOAuth2Flow, "finish", mock_dropbox_finish)
  
  client.get('/dropbox/finish', query_string=query_string)
  assert session['dropbox-access-token'] == oauth2flow_result.access_token
    
    
def test_dropbox_oauth_finish_handles_badrequestexception(client):
  response = client.get('/dropbox/finish')
  assert response.status_code == 400
    
def test_dropbox_oauth_finish_handles_badstateexception(client):
  """
  This test triggers a BadStateException by not setting
  session['dropbox-auth-csrf-token'] before requesting
  /dropbox/finish
  """
  
  query_string = { 'state': 'sojhqf2nGunEIxI', 'code': 'pQbO_7SMV2AAAAAAAAAAL'}
  response = client.get('/dropbox/finish', query_string=query_string)
  
  expected = { 'path': '/dropbox/start', 'code': 302 }
  
  assert response.status_code == expected['code']
  assert urlparse(response.location).path == expected['path']

def test_dropbox_oauth_finish_handles_csrfexception(client):
  with client.session_transaction() as sess:
    sess['dropbox-auth-csrf-token'] = 'sojhqf2nGunEIxI-MdePeg%3D%3D'
    
  query_string = { 'state': 'sojhqf2nGunEIxI', 'code': 'pQbO_7SMV2AAAAAAAAAAL'}
  response = client.get('/dropbox/finish', query_string=query_string)
  
  expected_code = 403
  assert response.status_code == expected_code
  
def test_dropbox_oauth_finish_handles_notapprovedexception(client):
  query_string = {
    'state': '6v9KgpO7jf9m5hATX_ujsg%3D%3D',
    'error_description': 'The+user+chose+not+to+give+your+app+access+to+their+Dropbox+account.',
    'error': 'access_denied'
  }
  
  with client.session_transaction() as sess:
    sess['dropbox-auth-csrf-token'] = query_string['state']
  
  response = client.get('/dropbox/finish', query_string=query_string)
  data = response.get_json()
  
  assert data['error'] == 'access_denied'