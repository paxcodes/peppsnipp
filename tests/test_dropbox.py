from application import create_app
from urllib.parse import urlparse

 
def test_dropbox_oauth_start():
  app = create_app()
  with app.test_client() as client:
    response = client.get('/dropbox/start')
    
    expectedNetworkLocation = "www.dropbox.com"
    assert response.status_code == 302
    assert urlparse(response.location).netloc == expectedNetworkLocation
