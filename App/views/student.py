from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import *

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/students/<string:username>/rankings', methods=['GET'])
def get_historical_student_rankings(username):
    response = get_rank_history_json(username)
    if response:
        return response
    else:
        return (jsonify({'error':"student does not exist"}), 404)