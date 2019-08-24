from flask import Flask
from application import dropbox
from dotenv import load_dotenv

def create_app():
  load_dotenv()
  app = Flask(__name__, instance_relative_config=False)
  app.config.from_object('config.Config')

  with app.app_context():
    app.register_blueprint(dropbox.dropbox_blueprint)

    return app