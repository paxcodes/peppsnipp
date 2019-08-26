from flask import Blueprint, jsonify, session

dropbox_blueprint = Blueprint('dropbox_blueprint', __name__)
 
@dropbox_blueprint.route('/dropbox', methods=['GET'])
def hello_dropbox():
  session['message'] = 'Hello World!'
  return jsonify({
      "msg": "Hello Dropbox!"
  })