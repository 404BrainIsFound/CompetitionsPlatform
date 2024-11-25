from App.database import db
from abc import ABC, abstractmethod

class ScoreManager:
    # id = db.Column(db.Integer, primary_key = True)
    # team_result = db.Column(db.Integer, db.ForeignKey('competition_team.id'), nullable = False)
    
    @abstractmethod
    def update_scores(self):
        pass