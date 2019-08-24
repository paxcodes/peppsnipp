from flask import Flask
from application import dropbox

def create_app():
  app = Flask(__name__)

  with app.app_context():
    app.register_blueprint(dropbox.dropbox_blueprint)

    return app