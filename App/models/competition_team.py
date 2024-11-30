from App.database import db
from .score_manager import *
from .student import *
from .team import *


class CompetitionTeamManager(db.Model):
    __tablename__ = 'competition_team_managers'
    
    id = db.Column(db.Integer, primary_key=True)
    competition_team_id = db.Column(db.Integer, db.ForeignKey('competition_team.id'), nullable=False)
    manager = db.Column(db.String, nullable=False)
    competition_team = db.relationship('CompetitionTeam', back_populates='managers')
    
    def __init__(self, competition_team_id, manager):
        self.competition_team_id = competition_team_id
        self.manager = manager


class CompetitionTeam(db.Model):
    __tablename__ = 'competition_team'
    
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    team_id =  db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    points_earned = db.Column(db.Integer, default=0)
    rating_score = db.Column(db.Integer, default=0)
    managers = db.relationship('CompetitionTeamManager', back_populates='competition_team', cascade="all, delete-orphan")

    def __init__(self, comp_id, team_id):
        self.comp_id = comp_id
        self.team_id = team_id
        self.points_earned = 0
        self.rating_score = 0
        
        try:
            team = Team.query.filter_by(id=team_id).first()
            for student in team.students:
                self.attach(student)
        except Exception as e:
            print(f'Error initializing managers: {e}')
    
    def attach(self, manager : ScoreManager):
        student = next((m for m in self.managers if m.manager == manager.username), None)
        if not student:
            print(f'Attaching manager {manager.username}')
            new_manager = CompetitionTeamManager(competition_team_id=self.id, manager=manager.username)
            self.managers.append(new_manager)
            try:
                db.session.add(new_manager)
                db.session.commit()
            except Exception as e:
                print(f'Error attaching manager: {e}')
                db.session.rollback()
        else:
            print(f'Manager {manager.username} already attached')
    
    def detach(self, manager : ScoreManager):
        student = next((m for m in self.managers if m.manager == manager.username), None)
        if student:
            print(f'Detaching manager {manager.username}')
            self.managers.remove(student)
            try:
                db.session.add(self)
                db.session.commit()
            except Exception as e:
                print(f'Error detaching manager: {e}')
                db.session.rollback()
        else:
            print(f'Manager {manager.username} not found in team')

    def notify(self):
        count = 0
        print(f'Notifying {len(self.managers)} managers.')
        for m in self.managers:
            count +=1
            print(f'Notifying manager {count}: {m.manager}')
            student = Student.query.filter_by(username=m.manager).first()
            if student:
                try:
                    student.update(self.rating_score)
                    db.session.add(student)
                    db.session.commit()
                except Exception as e:
                    print(f'Error updating manager: {e}')
                    db.session.rollback()
            else:
                print(f'Student with username {m.manager} not found')

    def update_points(self, points_earned):
      self.points_earned = points_earned
      db.session.add(self)
      db.session.commit()

    def update_rating(self, rating_score):
      self.rating_score = rating_score
      db.session.add(self)
      db.session.commit()

    def get_json(self):
      return {
          "id" : self.id,
          "team_id" : self.team_id,
          "competition_id" : self.comp_id,
          "points_earned" : self.points_earned,
          "rating_score" : self.rating_score
      }

    def toDict(self):
        return {
            "ID" : self.id,
            "Team ID" : self.team_id,
            "Competition ID" : self.comp_id,
            "Points Earned" : self.points_earned,
            "Rating Score" : self.rating_score
        }