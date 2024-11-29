from flask import Blueprint, jsonify
from flask_jwt_extended import current_user as jwt_current_user

from App.controllers import *

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/students/<string:name>/rankings', methods=['GET'])
def get_historical_student_rankings(name):
    response = get_rank_history_json(name)
    if response:
        return response
    else:
        return (jsonify({'error':"student does not exist"}), 404)