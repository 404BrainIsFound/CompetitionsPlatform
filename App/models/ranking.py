from App.database import db
from .score_manager import *

class Ranking(db.Model, ScoreManager):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    rank = db.Column(db.Integer)

    def __init__(self, student_id):
        self.student_id = student_id
    
    def update_rankings(self, rank):
        self.rank = rank
