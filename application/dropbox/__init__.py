from flask import Blueprint, jsonify, session, redirect
from flask import current_app as app
from dropbox.oauth import *

dropbox_blueprint = Blueprint('dropbox_blueprint', __name__)
 
@dropbox_blueprint.route('/dropbox', methods=['GET'])
def hello_dropbox():
  session['message'] = 'Hello World!'
  return jsonify({
      "msg": "Hello Dropbox!"
  })

@dropbox_blueprint.route('/dropbox/start')
def dropbox_oauth_start():
  authorize_url = get_dropbox_auth_flow().start()
  return redirect(authorize_url)
  
def get_dropbox_auth_flow():
  DROPBOX_APP_KEY = app.config['DROPBOX_APP_KEY']
  DROPBOX_APP_SECRET = app.config['DROPBOX_APP_SECRET']
  REDIRECT_URI = app.config['URL'] + "/dropbox/finish"
  return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, 
    REDIRECT_URI, session, "dropbox-auth-csrf-token")
  