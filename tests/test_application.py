from application import create_app

def test_appLoadsConfig():
  app = create_app()
  assert app.config['FLASK_APP'] == "Pepperplate Snipper"
