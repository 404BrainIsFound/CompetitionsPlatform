from App.database import db
from App.models import Student, Competition, Notification, CompetitionTeam, Ranking

def create_student(username, password, email):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password, email=email)
    try:
        db.session.add(newStudent)
        db.session.commit()
        print(f'New Student: {username} created!')
        return newStudent
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None


def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json


def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        try:
            db.session.add(student)
            db.session.commit()
            print("Username was updated!")
            return student
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None


def display_student_info(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None

    competitions = []
    
    for team in student.teams:  # Iterate over the teams the student belongs to
        team_comps = CompetitionTeam.query.filter_by(team_id=team.id).all()  # Get competition-team relationships
        for comp_team in team_comps:
            comp = Competition.query.filter_by(id=comp_team.comp_id).first()  # Fetch competition details
            competitions.append({
                "name": comp.name,
                "team": team.name,  
                "points_earned": comp_team.points_earned,
                "rating_score": comp_team.rating_score,
            })

    profile_info = {
        "profile": student.get_json(),
        "competitions": competitions
    }

    return profile_info


def display_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return {"notifications":[notification.to_Dict() for notification in student.notifications]}


def create_ranking(student_id, rank, date):
    ranking = Ranking(student_id, rank, date)
    
    try:
        db.session.add(ranking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'Error creating ranking: {e}')


def create_notification(student):
    if student.prev_rank == 0:
        message = f'RANK : {student.curr_rank}. Congratulations on your first rank!'
    elif student.curr_rank == student.prev_rank:
        message = f'RANK : {student.curr_rank}. Well done! You retained your rank.'
    elif student.curr_rank < student.prev_rank:
        message = f'RANK : {student.curr_rank}. Congratulations! Your rank has went up.'
    else:
        message = f'RANK : {student.curr_rank}. Oh no! Your rank has went down.'
    
    notification = Notification(student.id, message)
    student.notifications.append(notification)
    
    try:
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'Error updating student notifications: {e}')


def update_rankings(comp_name):
    students = get_all_students()
    competition = Competition.query.filter_by(name=comp_name).first()

    if not students:
        print("No students exist!")
        return []
    elif not competition:
        print(f'No competition named {comp_name} exists!')
        return []
    
    students.sort(key=lambda x: (x.rating_score), reverse=True)

    leaderboard = []
    count = 1
    
    curr_high = students[0].rating_score
    curr_rank = 1
    
    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            count += 1

            student.prev_rank = student.curr_rank
            student.curr_rank = curr_rank
            if student.prev_rank == 0:
                message = f'RANK : {student.curr_rank}. Congratulations on your first rank!'
            elif student.curr_rank == student.prev_rank:
                message = f'RANK : {student.curr_rank}. Well done! You retained your rank.'
            elif student.curr_rank < student.prev_rank:
                message = f'RANK : {student.curr_rank}. Congratulations! Your rank has went up.'
            else:
                message = f'RANK : {student.curr_rank}. Oh no! Your rank has went down.'
            
            create_ranking(student.id, student.curr_rank, competition.date)
            create_notification(student)

            try:
                db.session.add(student)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        else:
            create_ranking(student.id, 0, competition.date)

    return leaderboard


def display_rankings():
    students = get_all_students()

    if not students:
        print("No students exist!")
        return []

    students.sort(key=lambda x: (x.rating_score), reverse=True)

    leaderboard = []
    count = 1
    curr_high = students[0].rating_score
    curr_rank = 1
        
    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            count += 1

    print("Rank\tStudent\tRating Score")

    for position in leaderboard:
        print(f'{position["placement"]}\t{position["student"]}\t{position["rating score"]}')
    
    return leaderboard


def display_rank_history(username):
    student = get_student_by_username(username)

    if not student:
        print(f'Student {username} does not exist!')
        return
    
    history = Ranking.query.filter_by(student_id=student.id).all()
    history.sort(key=lambda x: (x.id), reverse=True)
    
    print("Rank\t Date")
    
    for rank in history:
        if rank.rank == 0:
            print(f'Unranked {rank.date}')
        else:
            print(f'{rank.rank}\t {rank.date}')


def get_rank_history_json(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return
    
    history = Ranking.query.filter_by(student_id=student.id).all()

    if not history:
        return []
    else:
        history.sort(key=lambda x: (x.id), reverse=True)
        return [rank.get_json() for rank in history]