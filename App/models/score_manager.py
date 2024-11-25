from App.database import db

class ScoreManager(db.Model):
    __tablename__ = 'score_manager'

    id = db.Column(db.Integer, primary_key = True)
    team_result = db.Column(db.Integer, db.ForeignKey('competition_team.id'), nullable = False)

    def __init__(self, team_result):
        self.team_result = team_result
    
    def update_scores(self):
        pass