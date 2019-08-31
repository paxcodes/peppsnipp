from dropbox.oauth import OAuth2FlowResult, DropboxOAuth2Flow
from application import create_app
from urllib.parse import urlparse
from flask import session

 
def test_dropbox_oauth_start():
  app = create_app()
  with app.test_client() as client:
    response = client.get('/dropbox/start')
    
    expectedNetworkLocation = "www.dropbox.com"
    assert response.status_code == 302
    assert urlparse(response.location).netloc == expectedNetworkLocation
    

def test_dropbox_oauth_finish(monkeypatch):
  app = create_app()
  with app.test_client() as client:
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
    
    # Mock whatever finish returns.
    client.get('/dropbox/finish', query_string=query_string)
    assert session['dropbox-access-token'] == oauth2flow_result.access_token
    
    
  
