from flask import Blueprint
from flask import jsonify
from flask import request

from peppcrawler import PepperplateCrawler

pepperplate_blueprint = Blueprint('pepperplate_blueprint', __name__)


@pepperplate_blueprint.route('/pepperplate/session', methods=['POST'])
def login():
    crawler = PepperplateCrawler()
    crawler.Login(request.form['email'], request.form['password'])
    return jsonify({
        "recipeTotal": crawler.GetRecipeTotal(),
        "usersName": crawler.GetUsersName()
    })
