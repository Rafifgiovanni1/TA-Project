from .. import db

class Student(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50),nullable=False)
    major: str = db.Column(db.String(50),nullable=False)
    score: int = db.Column(db.Integer,nullable=False)
    extra_activity: str = db.Column(db.String(50),nullable=False)
    academic_achievement: str = db.Column(db.String(50),nullable=False)
    nonacademic_achievement: str = db.Column(db.String(50),nullable=False)
    accept_status: bool = db.Column(db.Boolean)

    def __repr__(self):
        return f"Murid {self.id} "

    def __init__(self,name: str,major: str,score: int,extra_activity: str,academic_achivement: str,nonacademic_achivement: str,accept_status: bool):
        self.name = name
        self.major = major
        self.score = score
        self.extra_activity = extra_activity
        self.academic_achievement = academic_achivement
        self.nonacademic_achievement = nonacademic_achivement
        self.accept_status = accept_status
        # self._class = _class
    def add(self):
        db.session.add(self)
        db.session.commit()


