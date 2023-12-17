from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField,PasswordField,SelectField,SubmitField,DateField,EmailField,FileField
from wtforms.validators import DataRequired,Length,EqualTo,Regexp,ValidationError

class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),Length(min=1,max=35)],
                           render_kw={"class": "form-control","placeholder": "Username"} )
    password = PasswordField("Password",
                            validators=[DataRequired(),Length(min=1,max=35)],
                            render_kw={"class": "form-control","placeholder": "Password"})
    submit = SubmitField("Login")

class StudentForm(FlaskForm):
    name = StringField("Nama murid",validators=[DataRequired(),Length(min=5,max=60)],render_kw={"class": "form-control","placeholder": "Nama siswa"})
    major = SelectField("Jurusan",choices=["XII IPA 1","XII IPA 2","XII IPA 3","XII IPA 4","XII IPA 5","XII IPA 6","XII IPS 1","XII IPS 2"])
    score = IntegerField("Nilai",validators=[DataRequired()],render_kw={"class": "form-control"})
    extra_activity = SelectField("Keaktifan ekstrakulikuler",choices=["iya","tidak"])
    academic_achievement = SelectField("Prestasi akademik",choices=["iya","tidak"])
    nonacademic_achievement = SelectField("Prestasi nonakademik",choices=["iya","tidak"])
    accept_status = BooleanField("Status diterima")

class EditAccountForm(FlaskForm):
    password1 = PasswordField("Masukan password baru",validators=[DataRequired(),Length(min=8,max=50)],render_kw={"class": "form-control w-50","placeholder": "Password"})
    password2 = PasswordField("Masukan password lagi",validators=[DataRequired(),Length(min=8,max=50),EqualTo("password1",message="Password tidak sama")],render_kw={"class": "form-control w-50","placeholder": "Masukan password lagi"})
    email = EmailField("Email",validators=[DataRequired()],render_kw={"class": "form-control w-50","placeholder": "Email"})
    submit  = SubmitField("Edit akun")

class AddUserForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=5,max=50)],render_kw={"class": "form-control","placeholder": "Password"})
    password1 = PasswordField("Masukan password",validators=[DataRequired(),Length(min=8,max=50)],render_kw={"class": "form-control","placeholder": "Password"})
    password2 = PasswordField("Masukan password lagi",validators=[DataRequired(),Length(min=8,max=50),EqualTo("password1",message="Password tidak sama")],render_kw={"class": "form-control","placeholder": "Masukan password lagi"})
    email = EmailField("Email",render_kw={"class": "form-control mx-auto","placeholder": "Email"})
    submit  = SubmitField("Tambah user")

class StudentGradeForm(FlaskForm):
    class_name = SelectField("Kelas",choices=[x for x in range(1,7) ],render_kw={"class": "form-select","placeholder": "Semester"})
    semester = SelectField("Semester",choices=[("1","Semester 1"),("2","Semester 2")],render_kw={"class": "form-select","placeholder": "Semester"})
    subject = SelectField("Mata pelajaran",choices=["Nilai sikap","Agama","Pkn","B.indo","Mm","Ipa","Ips","Sbk","Pjok","B.ing"],render_kw={"class": "form-select","placeholder": "Semester"})

class StudentGradeSemesterForm(FlaskForm):
    class_name = SelectField("Kelas",choices=[x for x in range(1,7) ],render_kw={"class": "form-select","placeholder": "Semester"})
    semester = SelectField("Semester",choices=[("1","Semester 1"),("2","Semester 2")],render_kw={"class": "form-select","placeholder": "Semester"})

class StudentDataFile(FlaskForm):
    student_data = FileField(validators=[DataRequired("File kosong")],render_kw={"class": "form-control","accept": ".xlsx"})
