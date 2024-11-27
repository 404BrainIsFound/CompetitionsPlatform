from App.database import db

class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    rank = db.Column(db.Integer, nullable = False)

    def __init__(self, student_id, rank):
        self.student_id = student_id
        self.rank = rank
