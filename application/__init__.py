from flask import Flask
from flask_session import Session
from dotenv import load_dotenv

sess = Session()

def create_app():
  load_dotenv()
  app = Flask(__name__, instance_relative_config=False)
  app.config.from_object('config.Config')

  sess.init_app(app)
  
  with app.app_context():
    from application import main
    from application import dropbox
    
    app.register_blueprint(main.main_blueprint)
    app.register_blueprint(dropbox.dropbox_blueprint)

    return app