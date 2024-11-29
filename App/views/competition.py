from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, session
from flask_jwt_extended import current_user as jwt_current_user
from flask_login import current_user, login_required
#from datetime import datetime

from.index import index_views

from App.controllers import *

comp_views = Blueprint('comp_views', __name__, template_folder='../templates')

##return the json list of competitions fetched from the db
@comp_views.route('/competitions', methods=['GET'])
def get_competitions():
    competitions = get_all_competitions_json()
    return render_template('competitions.html', competitions=get_all_competitions(), user=current_user)

#create new comp
@comp_views.route('/competitions', methods=['POST'])
@login_required
def create_comp():
    data = request.form
    
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None

    date = data['date']
    date = date[8] + date[9] + '-' + date[5] + date[6] + '-' + date[0] + date[1] + date[2] + date[3]
    
    response = create_competition(moderator.username, data['name'], date, data['location'], data['level'], data['max_score'])
    if response:
        flash("Added Competition!", "success")
    else:
        flash("Error adding Competition","error")
    return render_template('competitions.html', competitions=get_all_competitions(), user=current_user)

#page to create new comp
@comp_views.route('/competitions/new-competition', methods=['GET'])
@login_required
def create_comp_page():
    if session['user_type'] == 'moderator':
        return render_template('competition_creation.html', user=current_user)
    else:
        return (jsonify({'error':"insufficient permissions"}), 401)

@comp_views.route('/competitions/<string:name>', methods=['GET'])
def competition_details(name):
    competition = get_competition_by_name(name)
    if not competition:
        return render_template('404.html')
    
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(competition.name)
    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)#, team=team)

#page to comp upload comp results   - to get details first
@comp_views.route('/competitions/<string:name>/results', methods=['GET'])
def add_results_page(name):
    competition = get_competition_by_name(name)
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None

    leaderboard = display_competition_results(competition.name)

    return render_template('competition_results.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)

@comp_views.route('/competitions/<string:name>/results', methods=['POST'])
def add_competition_results(name):
    competition = get_competition_by_name(name)
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None
        
    data = request.form
    
    team_name = data['team_name']
    students = [data['student1'], data['student2'], data['student3']]

    for student_name in students:
        student = get_student_by_username(student_name)                             #validate student
        if not student:
            flash(f"Student '{student_name}' does not exist!", "error")
            return redirect(url_for('comp_views.add_results_page', comp_id=competition.id))

    if int(data['score']) > get_competition_max_val(name):                  #added this to ensure not more than max
        flash(f"Score is more than max score for competition", "error")
        return redirect(url_for('comp_views.add_results_page', comp_id=competition.id))

    response = add_team(moderator.username, name, team_name, students)

    if response:
        response = add_results(moderator.username, name, team_name, int(data['score']))
        if response:
            flash("Results added successfully!", "success")
        else:
            flash("Failed to add results!", "error")
    else:
        flash("Failed to add team!", "error")
    
    leaderboard = display_competition_results(name)

    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)
    
@comp_views.route('/competitions/<string:name>/final-results', methods=['GET'])
def confirm_results(name):
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None
    
    competition = get_competition_by_name(name)

    if update_ratings(moderator.username, competition.name):
        update_rankings(name)

    leaderboard = display_competition_results(name)

    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)

@comp_views.route('/competitions_postman', methods=['GET'])
def get_competitions_postman():
    competitions = get_all_competitions_json()
    return (jsonify(competitions),200)

@comp_views.route('/createcompetition_postman', methods=['POST'])
def create_comp_postman():
    data = request.json
    response = create_competition('robert', data['name'], data['date'], data['location'], data['level'], data['max_score'])
    if response:
        return (jsonify({'message': "Competition created!"}), 201)
    return (jsonify({'error': "Error creating competition"}),500)

@comp_views.route('/competitions_postman/<int:id>', methods=['GET'])
def competition_details_postman(id):
    competition = get_competition(id)
    if not competition:
        return (jsonify({'error': "Competition not found"}),404)
    
    
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(competition.name)
    return (jsonify(competition.toDict()),200)

@comp_views.route('/add_results_postman/<string:comp_name>', methods=['POST'])
def add_competition_results_postman(comp_name):
    competition = get_competition_by_name(comp_name)
    
    data = request.json
    
    students = [data['student1'], data['student2'], data['student3']]
    response = add_team('robert', comp_name, data['team_name'], students)

    if response:
        response = add_results('robert', comp_name, data['team_name'], int(data['score']))
    if response:
        return (jsonify({'message': "Results added successfully!"}),201)
    return (jsonify({'error': "Error adding results!"}),500)