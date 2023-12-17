from flask import Blueprint,request,redirect,current_app,send_from_directory,flash,url_for,render_template
from flask_login import current_user
from jinja2 import Template
from plotly.express import pie,bar
from plotly.utils import PlotlyJSONEncoder
from json import  loads,dumps
from ..model.students import Student
from ..utils.forms import StudentGradeSemesterForm
import pandas as pd
import pdfkit
import pickle
import os
import subprocess

student = Blueprint("student",__name__)

@student.route("/",methods=["GET","POST"])
def index():
	SUBJECT = ["Agama","Pkn","B.indo","Mm","Ipa","Ips","Sbk","Pjok","B.ing"]

	class_name = request.args.get("class_name","1")
	semester_name = request.args.get("semester_name","1")
	download_pdf = request.args.get("download_pdf",False)

	forms: StudentGradeSemesterForm = StudentGradeSemesterForm()

	if request.method == "POST" and forms.validate_on_submit():
		return redirect(url_for("student.index",class_name=forms.class_name.data,semester_name=forms.semester.data))

	current_student: Student = Student.query.filter_by(nik=current_user.username).first()
	student_scores = loads(current_student.scores) if current_student.scores else {}
	scores_data = []

	student_class = student_scores.keys()
	for subject in SUBJECT:
		for _class in student_class:
			semesters = student_scores[_class].keys()
			for semester in semesters:
				avg = 0

				try:
					scores = student_scores[_class][semester]["scores"]
					semester_scores = student_scores[_class][semester]["semester_score"].get(subject.lower(),0)
				except KeyError:
					scores = {}
					semester_scores = {}

				avg = (((scores[subject.lower()]["tugas 1"] + scores[subject.lower()]["tugas 2"] + scores[subject.lower()]["tugas 3"] + scores[subject.lower()]["tugas 4"])  / 4 ) + ((scores[subject.lower()]["Ulangan 1"] + scores[subject.lower()]["Ulangan 2"])  / 2))  / 2
				avg = (avg + semester_scores) / 2

				scores_dict = {"subject": subject,"average": avg,"class_semester": f"{_class} {semester}"}
				scores_data.append(scores_dict)


	scores_data = pd.DataFrame(scores_data)

	scores: dict = loads(current_student.scores).get(class_name,{}).get(f"semester{semester_name}",{}) if current_student.scores else {}
	test_and_task = scores.get("scores",{})
	semester_score = scores.get("semester_score",{})

	data_score = {}

	try:
		data_score = scores_data[scores_data["class_semester"] == f"{class_name} semester{semester_name}"]

		fig = bar(data_score,x="subject",y="average",title="NIlai rata rata",color="subject")
		bar_json = dumps(fig,cls=PlotlyJSONEncoder)
	except:
		bar_json = None

	total_sum_average = sum(list(data_score["average"]))
	total_average = total_sum_average / 9
	presention = loads(current_student.presention).get(class_name,{}).get(f"semester{semester_name}",{}) if current_student.presention else {}
	presention_percentage = ((150 - (presention.get("S",0) + presention.get("I",0) + presention.get("A",0))) / 150) * 100
	grading = "-"

	with open("src/encoder.pkl", "rb") as f:
		encoder = pickle.load(f)

	with open("src/ml.pkl","rb") as f:
		ml = pickle.load(f)

	with open("src/_ml.pkl","rb") as f:
		_ml = pickle.load(f)


	if len(data_score) > 0:
		label_encode = {
			"B": 0,
			"C": 1,
			"SB": 2
		}

		discipline = test_and_task.get("displin","-")
		attitude = test_and_task.get("percayadiri","-")
		print(list(data_score["average"]))
		input_arr = [[*list(data_score["average"]),label_encode.get(discipline,1), label_encode.get(attitude,1),presention_percentage]]


		grading = ml.predict(input_arr)

	if download_pdf:
		template = Template(open("app/templates/student/print_report.html","r").read())
		template = template.render(current_student=current_student,test_and_task=test_and_task,semester_score=semester_score,forms=forms,submit_url="student.index",presention=presention,class_name=class_name,url_for=url_for,total_average=total_average,total_sum_average=total_sum_average,grading=grading[0],semester_name=semester_name,bar_json=bar_json,subjects=["agama", "pkn", "b.indo", "mm", "ipa", "ips", "sbk", "pjok", "b.ing"])
		try:
			output = subprocess.check_output(['wkhtmltopdf', '--version'])
		except subprocess.CalledProcessError:
			flash("wkhtmltopdf belum terinstall, harap install wkthtmltopdf sesuai dengan sistem")
		else:
			pdf_path = os.path.join(current_app.root_path,"pdf")
			pdfkit.from_string(template, f"{pdf_path}/{current_student.nik}_{class_name}_semester{semester_name}.pdf")


		return send_from_directory(current_app.root_path,f"pdf/{current_student.nik}_{class_name}_semester{semester_name}.pdf",as_attachment=True)

	return render_template("student/index.html",current_student=current_student,test_and_task=test_and_task,semester_score=semester_score,forms=forms,submit_url="student.index",presention=presention,class_name=class_name,total_average=total_average,total_sum_average=total_sum_average,grading=grading[0],semester_name=semester_name,bar_json=bar_json,subjects=["agama", "pkn", "b.indo", "mm", "ipa", "ips", "sbk", "pjok", "b.ing"])
