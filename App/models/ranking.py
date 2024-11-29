from App.database import db
from datetime import datetime

class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    rank = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, student_id, rank, date):
        self.student_id = student_id
        self.rank = rank
        self.date = date

    def get_json(self):
        return {
            "student_id": self.student_id,
            "rank": self.rank,
            "date": self.date
        }