from flask import Blueprint, jsonify, session, redirect, request
from flask import current_app as app
from flask_cors import cross_origin

from application.api_error import APIError
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


@dropbox_blueprint.route('/dropbox/finish')
@cross_origin(methods='GET', origins=app.config['CLIENT_URL'], supports_credentials=True)
def dropbox_oauth_finish():
  try:
    oauth_result = get_dropbox_auth_flow().finish(request.args)
    session['dropbox-access-token'] = oauth_result.access_token
    return jsonify({
      "success": True,
    })
  except BadRequestException as e:
    error_message = e.args[0]
    raise APIError(error_message)
  except BadStateException:
    return redirect("/dropbox/start")
  except CsrfException as e:
    raise APIError("API encountered an error", 403)
  except NotApprovedException:
    return jsonify({
      "success": False,
      "message": "You did not give us permission to access your Dropbox account.",
      "error": request.args['error']
    })
    
  
def get_dropbox_auth_flow():
  DROPBOX_APP_KEY = app.config['DROPBOX_APP_KEY']
  DROPBOX_APP_SECRET = app.config['DROPBOX_APP_SECRET']
  REDIRECT_URI = app.config['CLIENT_URL'] + "/dropbox-finish"
  return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, 
    REDIRECT_URI, session, "dropbox-auth-csrf-token")
  