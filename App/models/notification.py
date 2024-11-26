from App.database import db

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    
    def __init__(self, student_id, message):
      self.student_id = student_id
      self.message = message

    def get_json(self):
      return {
            "id" : self.id,
            "student_id" : self.student_id,
            "notification" : self.message
      }

    def to_Dict(self):
      return {
            "ID" : self.id,
            "Notification" : self.message
      }
  
    def __repr__(self):
      return f'<Notification {self.id} : {self.message}>'