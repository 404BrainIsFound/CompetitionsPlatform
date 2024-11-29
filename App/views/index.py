from flask import Blueprint, render_template, jsonify, session
from flask_jwt_extended import current_user as jwt_current_user
from flask_login import current_user
from App.models import db
from App.controllers import *
import csv

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def home_page():
    return render_template('leaderboard.html', leaderboard=display_rankings(), user=current_user)

@index_views.route('/leaderboard', methods=['GET'])
def leaderboard_page():
    return render_template('leaderboard.html', leaderboard=display_rankings(), user=current_user)#, competitions=get_all_competitions(), moderators=get_all_moderators())


# creates students
def initialize_students():
    with open("students.csv") as student_file:
        reader = csv.DictReader(student_file)
        for student in reader:
            stud = create_student(student['username'], student['password'], student['email'])
    student_file.close()

# creates moderators
def initialize_moderators():
    with open("moderators.csv") as moderator_file:
        reader = csv.DictReader(moderator_file)
        for moderator in reader:
            mod = create_moderator(moderator['username'], moderator['password'], moderator['email'])
    moderator_file.close()

# creates competitions
def initialize_competitions():
    with open("competitions.csv") as competition_file:
        reader = csv.DictReader(competition_file)
        for competition in reader:
            comp = create_competition(competition['mod_name'], competition['comp_name'], competition['date'], competition['location'], competition['level'], competition['max_score'])
    competition_file.close()

# creates results
def initialize_results():
    with open("results.csv") as results_file:
        reader = csv.DictReader(results_file)
        for result in reader:
            students = [result['student1'], result['student2'], result['student3']]
            team = add_team(result['mod_name'], result['comp_name'], result['team_name'], students)
            add_results(result['mod_name'], result['comp_name'], result['team_name'], int(result['score']))
    results_file.close()

# finalizes results
def finalize_results():
    with open("competitions.csv") as competitions_file:
        reader = csv.DictReader(competitions_file)
        for competition in reader:
            if competition['comp_name'] != 'TopCoder':
                update_ratings(competition['mod_name'], competition['comp_name'])
                update_rankings(competition['comp_name'])    
    competitions_file.close()


@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    initialize_students()
    initialize_moderators()
    initialize_competitions()
    initialize_results()
    finalize_results()

    return render_template('leaderboard.html', leaderboard=display_rankings(), user=current_user)
    """
@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/healthcheck', methods=['GET'])
def health():
    return jsonify({'status':'healthy'})

#@index_views.route('/Student_Profile/<int:user_id>')
#def Student_Profile(user_id):
 #   return render_template('Student_Profile.html', user_id=user_id)
"""

@index_views.route('/profile')
def profile():
    user_type = session['user_type']
    id = current_user.get_id()
    
    if user_type == 'moderator':
        user = get_moderator(id)
        template = moderator_profile(user.username)

    if user_type == 'student':
        user = get_student(id)
        template = student_profile(user.username)

    return template

@index_views.route('/students/<string:name>', methods=['GET'])
def student_profile(name):
    student = get_student_by_username(name)

    if not student:
        return render_template('404.html')
    
    profile_info = display_student_info(student.username)
    competitions = profile_info['competitions']

    return render_template('student_profile.html', student=student, competitions=competitions, user=current_user)

@index_views.route('/moderators/<string:name>', methods=['GET'])
def moderator_profile(name):   
    moderator = get_moderator_by_username(name)

    if not moderator:
        return render_template('404.html')

    return render_template('moderator_profile.html', moderator=moderator, user=current_user)

@index_views.route('/init_postman', methods=['GET'])
def init_postman():
    
    db.drop_all()
    db.create_all()
    
    initialize_students()
    initialize_moderators()
    initialize_competitions()
    initialize_results()
    finalize_results()

    return (jsonify({'message': "database_initialized"}),200)