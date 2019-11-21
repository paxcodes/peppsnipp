from flask import Blueprint, jsonify, session, redirect, request
from flask import current_app as app
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
def dropbox_oauth_finish():
    try:
        oauth_result = get_dropbox_auth_flow().finish(request.args)
    except BadRequestException as e:
        raise APIError(e)
    except BadStateException:
        return redirect("/dropbox/start")
    except CsrfException as e:
        raise APIError(e, status_code=403)
    except NotApprovedException as e:
        return jsonify({
            "success": False,
            "msg": ("Our app was not approved to connect with your "
                    "Dropbox account. However, the app needs to connect with "
                    "your Dropbox to upload the recipes. If you change your "
                    "mind, feel free to try again.")
        })
    except ProviderException as e:
        raise APIError(e, status_code=403)

    session['dropbox-access-token'] = oauth_result.access_token
    return jsonify({
        "success": True,
        "msg": "",
    })


def get_dropbox_auth_flow():
    DROPBOX_APP_KEY = app.config['DROPBOX_APP_KEY']
    DROPBOX_APP_SECRET = app.config['DROPBOX_APP_SECRET']
    REDIRECT_URI = app.config['CLIENT_URL'] + "/dropbox-finish"
    return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET,
                             REDIRECT_URI, session, "dropbox-auth-csrf-token")
