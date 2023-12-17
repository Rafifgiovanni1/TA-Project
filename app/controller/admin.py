from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from werkzeug.security import generate_password_hash
from flask_login import current_user,login_required
from plotly.express import pie,bar
from plotly.figure_factory import create_annotated_heatmap
from plotly.utils import PlotlyJSONEncoder
from json import dumps,loads
from ..model.user import User
from ..model.students import db, Student
from ..utils.forms import StudentForm,EditAccountForm,AddUserForm,StudentDataFile,StudentGradeForm,StudentGradeSemesterForm
from ..utils import is_admin,to_tables,check_files
from .process import Process
import pandas as pd
import traceback
import sys

admin = Blueprint("admin",__name__)

@admin.route("/",methods=["GET","POST"])
@login_required
@is_admin
def index():
    forms: EditAccountForm = EditAccountForm()

    if request.method == "POST" and forms.validate_on_submit():
        _user = User.query.filter_by(id=current_user.id).first()
        _user.password = generate_password_hash(forms.password1.data)
        flash("Password berhasil diperbaharui",category="success")
        return redirect(url_for("admin.index"))

    forms.email.data = current_user.email
    return render_template("admin/index.html",forms=forms)

@admin.route("/student")
def student():
    students = Student.query.all()

    id_url = "admin.edit_student"

    students = to_tables(students,drop_column=["_sa_instance_state"],reorder_column=["id","name","major","score","extra_activity","academic_achievement","nonacademic_achievement"],rename_column={"name": "Nama murid","major": "Jurusan","score": "Nilai raport","extra_activity": "Keaktifan ekskul","academic_achievement": "Prestasi akademik","nonacademic_achievement": "Prestasi non-academic"},id_url=id_url,url_id="id")

    return render_template("admin/tables.html", tables=students, add_url="admin.add_student", delAll_url="admin.delAll_student", add_button_text="Tambah murid baru", delAll_button_text="Hapus semua data", title="Murid")

@admin.route("/student/delAll",methods=["GET","POST"])
@is_admin
@login_required
def delAll_student():

    Student.query.delete()
    db.session.commit()

    flash(message=f"data murid telah dihapus ",category="danger")
    return redirect(url_for("admin.student"))

@admin.route("/student/add",methods=["GET","POST"])
@is_admin
@login_required
def add_student():
    forms: StudentDataFile = StudentDataFile()

    if request.method == "POST" and forms.validate_on_submit():
        files = request.files[forms.student_data.name]

        if files.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            flash("File harus berbentuk file excel",category="danger")
            return redirect(url_for("admin.add_student"))

        excel = pd.read_excel(files)
        _student = pd.DataFrame()
        try:
            try:
                _student = pd.DataFrame({"name": excel["nama"],"major": excel["jurusan"],"score": excel["nilai"],"extra_activity": excel["keaktifan_ekskul"],"academic_achievement": excel["prestasi_akademik"],"nonacademic_achievement": excel["prestasi_nonakademik"]})
            except KeyError as e:
                flash(f"kolom {e} tidak ada pada file excel",category="")
                return redirect(url_for("admin.add_student"))
        
            student = _student.to_dict(orient="records")
            print(student)
            db.session.bulk_insert_mappings(Student, student)
            db.session.commit()        
        except Exception as e:
            flash(f"error: {e}")
        else:
            return redirect(url_for("admin.student"))

    forms.student_data.label = "Tambah data murid"
    return render_template("admin/add.html",forms=forms,title="Tambah murid",btn_title="murid")

@admin.route("/student/edit/<int:id>",methods=["GET","POST"])
@is_admin
@login_required
def edit_student(id):
    forms: StudentForm = StudentForm()
    _student: Student = Student.query.filter_by(id=id).first()

    if request.method == "POST" and forms.validate_on_submit():
        _student.name = forms.name.data
        _student.major = forms.major.data
        _student.score = forms.score.data
        _student.extra_activity = forms.extra_activity.data
        _student.academic_achievement = forms.academic_achievement.data
        _student.nonacademic_achievement = forms.nonacademic_achievement.data           
        _student.accept_status = forms.accept_status.data

        db.session.commit()
        flash(f"Data murid {{_student.name}} berhasil diupdate",category="success")
        return redirect(url_for("admin.student"))                                            
    # _class = Student.query.all()
    # _class = pd.DataFrame([query.__dict__ for query in _class])

    forms.name.data = _student.name
    forms.major.data = _student.major    
    forms.score.data = _student.score
    forms.extra_activity.data = _student.extra_activity
    forms.academic_achievement.data = _student.academic_achievement
    forms.nonacademic_achievement.data = _student.nonacademic_achievement
    forms.accept_status.data = _student.accept_status

    return render_template("admin/add.html",forms=forms,title="Edit murid",edit=True,btn_title="murid",data=_student,id=id)

@admin.route("/student/classification")
def process():
    students = Student.query.all()    
    query = pd.DataFrame([student.__dict__ for student in students])

    print(query)
        
    if not students:
        flash("Data murid kosong",category="danger")
        return redirect(url_for("admin.student"))

    query = query.drop(["_sa_instance_state"],axis=1).reindex(["name","major","score","extra_activity","academic_achievement","nonacademic_achievement"],axis=1).rename({"extra_activity": "activity","academic_achievement": "achievement"},axis=1)


    process = Process(query)
    process.process()

    _data = list(process.data["accept_status"].value_counts())
    _label = ["Diterima","Tidak Diterima"]
    
    fig =  pie(process.data,names=_label,values=_data,title="persentase perkiraan diterima di smnptn")
    pie_json = dumps(fig,cls=PlotlyJSONEncoder)

    fig = bar(process.data,x=_label,y=_data,color=_label)
    bar_json = dumps(fig,cls=PlotlyJSONEncoder)

    data = process.data.rename({"name": "Nama","major": "Jurusan","score": "Nilai","activity": "Keaktifan ekskul","achievement": "Prestasi akademik","nonacademic_achievement": "Prestasi non-akademik","accept_status": "Diterima di snpmptn"},axis=1)    
    return render_template("student/index.html",table=data.to_html(table_id="table",classes=["table","table-hover"]),pie_json=pie_json,bar_json=bar_json)

@admin.route("/student/evaluate")
def evaluate():
    students = Student.query.all()
    query = pd.DataFrame([student.__dict__ for student in students])


    if not students:
        flash("Data murid kosong",category="danger")
        return redirect(url_for("admin.student"))


    query = query.drop(["_sa_instance_state"],axis=1).reindex(["name","major","score","extra_activity","academic_achievement","nonacademic_achievement"],axis=1).rename({"extra_activity": "activity","academic_achievement": "achievement"},axis=1)
    
    process = Process(query)
    process.process()

    confusion_matrix = process.confusion_matrix
    _confusion_matrix = create_annotated_heatmap(z=confusion_matrix.tolist(),x=["0","1"],y=["0","1"],colorscale="purp")
    plotly_json = dumps(_confusion_matrix,cls=PlotlyJSONEncoder)

    print(process.classification_score)

    return render_template("student/evaluate.html",plotly_json=plotly_json,score=process.score,classification_report=process.classification_score)

@admin.route("/student/delete/<int:id>")
@is_admin
@login_required
def delete_student(id):
    _student = Student.query.filter_by(id=id).first()

    db.session.delete(_student)
    db.session.commit()

    flash(message=f"data murid {_student} telah dihapus ",category="danger")
    return redirect(url_for("admin.student"))

@admin.route("/users")
@is_admin
@login_required
def user_page():
    users = User.query.filter(id != current_user.id ).all()
    users = to_tables(users,drop_column=["_sa_instance_state"],reorder_column=["username","email","role"])

    return render_template("admin/tables.html",tables=users,add_url="admin.user_add",add_button_text="Tambah user baru",title="User")

@admin.route("/users/add",methods=["GET","POST"])
@login_required
@is_admin
def user_add():
    forms: AddUserForm = AddUserForm()

    if request.method == "POST" and forms.validate_on_submit():
        user = User(forms.username.data,forms.email.data,forms.password1.data,"teacher")
        try:
            user.add()
        except:
            flash(f"User dengan emait atau username yang sama sudah ada",category="danger")
            return redirect(url_for("admin.user_add"))
        return redirect(url_for("admin.user_page"))

    return render_template("admin/add.html",forms=forms,title="Tambah user",btn_title="user")

@admin.route("/users/edit/<int:id>",methods=["GET","POST"])
@login_required
@is_admin
def user_edit(id):
    forms: AddUserForm = AddUserForm()
    _user: User = User.query.filter_by(id=id).first()

    forms.username.data = _user.username
    forms.email.data = _user.email
    forms.password1.data = ""
    forms.password2.data = ""

    return render_template("admin/add.html",forms=forms,title="Edit user",edit=True,btn_title="user")
