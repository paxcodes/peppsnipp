from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app as app
from flask_cors import cross_origin

from peppcrawler import PepperplateCrawler

pepperplate_blueprint = Blueprint('pepperplate_blueprint', __name__)


@pepperplate_blueprint.route('/pepperplate/session', methods=['POST'])
@cross_origin(methods='POST', origins=app.config['CLIENT_URL'], supports_credentials=True)
def login():
    crawler = PepperplateCrawler()
    crawler.Login(request.json['email'], request.json['password'])
    return jsonify({
        "recipeTotal": crawler.GetRecipeTotal(),
        "usersName": crawler.GetUsersName()
    })
