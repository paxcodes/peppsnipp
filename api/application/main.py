from flask import Blueprint, jsonify
from application.api_error import APIError

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.app_errorhandler(APIError)
def handle_apierror(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@main_blueprint.route('/', methods=['HEAD'])
def helloWorld():
    return "Hello!"
