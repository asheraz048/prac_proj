from db import db


class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    grade = db.Column(db.String(80))
    fee = db.Column(db.Integer)


    def __init__(self, name, grade, fee):
        self.name = name
        self.grade = grade
        self.fee = fee

    def json(self):
        return {'name': self.name, 'grade': self.grade ,'fee' : self.fee}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()