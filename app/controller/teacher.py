from flask import Blueprint,render_template
from ..model.students import Student
from ..utils.forms import StudentGradeForm

teacher = Blueprint("teacher",__name__)

@teacher.route("/")
def index():
    return render_template("teacher/index.html")

@teacher.route("/grade/<int:id>",methods=["GET","POST"])
def grade(id):
    _student = Student.query.filter_by(id=id).first()
    forms: StudentGradeForm = StudentGradeForm()
    

    return render_template("teacher/grade.html",forms=forms,id=id)