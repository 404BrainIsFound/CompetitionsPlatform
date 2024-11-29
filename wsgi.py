import csv
import click, pytest, sys
from flask import Flask
from datetime import datetime, date

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# create students
def initialize_students():
    with open("students.csv") as student_file:
        reader = csv.DictReader(student_file)
        for student in reader:
            stud = create_student(student['username'], student['password'], student['email'])
    student_file.close()

#creates moderators
def initialize_moderators():
    with open("moderators.csv") as moderator_file:
        reader = csv.DictReader(moderator_file)
        for moderator in reader:
            mod = create_moderator(moderator['username'], moderator['password'], moderator['email'])
    moderator_file.close()

#creates competitions
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
            update_ratings(competition['mod_name'], competition['comp_name'])
            update_rankings(competition['comp_name'])
    competitions_file.close()


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    initialize_students()
    initialize_moderators()
    initialize_competitions()
    initialize_results()
    finalize_results()

    print('database intialized')


'''
Student Commands
'''

student_cli = AppGroup("student", help="Student commands") 

@student_cli.command("create", help="Creates a student")
@click.argument("username", default="stud1")
@click.argument("password", default="stud1pass")
@click.argument("email", default="stud1mail")
def create_student_command(username, password, email):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    student = create_student(username, password, email)

@student_cli.command("update", help="Updates a student's username")
@click.argument("id", default="1")
@click.argument("username", default="stud1")
def update_student_command(id, username):
    id = input("Enter your ID number: ")
    username = input("Enter your username: ")
    student = update_student(id, username)

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default=1)
def list_students_command(format):
    print ("Select Format:")
    print ("1. String")
    print ("2. Json")
    format = input("Enter your choice: ")
    if format == "1":
        print(get_all_students())
    elif format == "2":
        print(get_all_students_json())
    else:
        print("That was an invalid choice!")

@student_cli.command("display", help="Displays student profile")
@click.argument("username", default="stud1")
def display_student_info_command(username):
    username = input("Enter your username: ")
    print(display_student_info(username))

@student_cli.command("notifications", help="Gets all notifications")
@click.argument("username", default="stud1")
def display_notifications_command(username):
    username = input("Enter your username: ")
    print(display_notifications(username))

@student_cli.command("rank", help="Gets the rank history of the student")
@click.argument("username", default="stud1")
def get_rank_history_command(username):
    username = input("Enter your username: ")
    print(get_rank_history_json(username))

app.cli.add_command(student_cli)


'''
Moderator Commands
'''

mod_cli = AppGroup("mod", help="Moderator commands") 

@mod_cli.command("create", help="Creates a moderator")
@click.argument("username", default="mod1")
@click.argument("password", default="mod1pass")
@click.argument("email", default="mod1mail")
def create_moderator_command(username, password, email):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    mod = create_moderator(username, password, email)

@mod_cli.command("display", help="Displays moderator profile")
@click.argument("username", default="mod1")
def display_moderator_info_command(username):
    username = input("Enter your username: ")

    mod = get_moderator_by_username(username)
    print(mod.get_json())

# @mod_cli.command("addMod", help="Adds a moderator to a competition")
# @click.argument("mod1_name", default="mod1")
# @click.argument("comp_name", default="comp1")
# @click.argument("mod2_name", default="mod2")
# def add_mod_to_comp_command(mod1_name, comp_name, mod2_name):
#     mod = add_mod(mod1_name, comp_name, mod2_name)


# @mod_cli.command("addTeam", help="Adds a team to a competition")
# @click.argument("mod_name", default="mod1")
# @click.argument("comp_name", default="comp1")
# @click.argument("team_name", default="A")
# @click.argument("student1", default="stud1")
# @click.argument("student2", default="stud2")
# @click.argument("student3", default="stud3")
# def add_team_to_comp_command(mod_name, comp_name, team_name, student1, student2, student3):
#     student1 = input ("Enter the name for Student 1: ")
#     student2 = input ("Enter the name for Student 2: ")
#     student3 = input ("Enter the name for Student 3: ")

#     mod_name = input ("Enter your username: ")
#     comp_name = input ("Enter the name of the competition: ")
#     team_name = input ("Enter the name of the team to be added: ")
    
    
#     students = [student1, student2, student3]
#     comp = add_team(mod_name, comp_name, team_name, students)


@mod_cli.command("addResults", help="Adds results for a team in a competition")
@click.argument("mod_name", default="mod1")
@click.argument("comp_name", default="comp1")
@click.argument("team_name", default="team1")
@click.argument("student1", default="stud1")
@click.argument("student2", default="stud2")
@click.argument("student3", default="stud3")
@click.argument("score", default=10)
def add_results_command(mod_name, comp_name, team_name, student1, student2, student3, score):
    student1 = input ("Enter the name for Student 1: ")
    student2 = input ("Enter the name for Student 2: ")
    student3 = input ("Enter the name for Student 3: ")

    mod_name = input ("Enter your username: ")
    comp_name = input ("Enter the name of the competition: ")
    team_name = input ("Enter the name of the team to be added: ")

    students = [student1, student2, student3]
    comp = add_team(mod_name, comp_name, team_name, students)

    score = input ("Enter the score for the team: ")
    score = int(score)

    if comp:
        comp_team = add_results(mod_name, comp_name, team_name, score)

@mod_cli.command("confirm", help="Confirms results for all teams in a competition")
@click.argument("mod_name", default="mod1")
@click.argument("comp_name", default="comp1")
def update_rankings_command(mod_name, comp_name):
    mod_name = input ("Enter your username: ")
    comp_name = input ("Enter the name of the competition: ")

    update_ratings(mod_name, comp_name)
    update_rankings(comp_name)

@mod_cli.command("rankings", help="Displays overall rankings")
def display_rankings_command():
    display_rankings()

@mod_cli.command("list", help="Lists moderators in the database")
@click.argument("format", default="1")
def list_moderators_command(format):
    print ("Select Format:")
    print ("1. String")
    print ("2. Json")
    format = input("Enter your choice: ")
    if format == "1":
        print(get_all_moderators())
    elif format == "2":
        print(get_all_moderators_json())
    else:
        print("An invalid selection was made!")
        

app.cli.add_command(mod_cli)


'''
Competition commands
'''

comp_cli = AppGroup("comp", help = "Competition commands")   

@comp_cli.command("create", help = "Creates a competition")
@click.argument("mod_name", default = "mod1")
@click.argument("name", default = "comp1")
@click.argument("date", default = "09-02-2024")
@click.argument("location", default = "CSL")
@click.argument("level", default = 1)
@click.argument("max_score", default = 25)
def create_competition_command(mod_name, name, date, location, level, max_score):

    mod_name = input("Enter the name of the competition moderator: ")
    name = input("Enter the name of the competition to be created: ")
    date = input("Enter the competiton date (mm-dd-yyyy): ")
    location = input("Enter the location: ")
    level = input("Enter the competiton level: ")
    max_score = input("Enter the competition's max score: ")

    level = int(level)
    max_score = int(max_score)
    
    comp = create_competition(mod_name, name, date, location, level, max_score)

@comp_cli.command("details", help = "Displays competition details")
@click.argument("name", default = "comp1")
def display_competition_details_command(name):
    name = input("Enter the name of the competition: ")
    comp = get_competition_by_name(name)
    print(comp.get_json())

@comp_cli.command("list", help = "list all competitions")
@click.argument("format", default="1")
def list_competition_command(format):
    
    print ("Select Format:")
    print ("1. String")
    print ("2. Json")
    format = input("Enter your choice: ")
    if format == "1":
        print(get_all_competitions())
    elif format == "2":
        print(get_all_competitions_json())
    else:
        print("An invalid selection was made!")

@comp_cli.command("results", help = "displays competition results")
@click.argument("name", default = "comp1")
def display_competition_results_command(name):
    name = input("Enter the name of the competition: ")
    print(display_competition_results(name))

app.cli.add_command(comp_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("app", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "IntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)


