from flask import Blueprint, jsonify

dropbox_blueprint = Blueprint('dropbox_blueprint', __name__)
 
@dropbox_blueprint.route('/dropbox', methods=['GET'])
def hello_dropbox():
  return jsonify({
      "msg": "Hello Dropbox!"
  })