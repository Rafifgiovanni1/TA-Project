from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError
from getpass import getpass
from ..model.user import User
from .. import app


@app.cli.command("createadmin")
def create_admin():
    """create new admin for the website"""
    username = input("admin username: ")
    password = getpass("admin password: ")
    password2 = getpass("repeat password: ")

    if password != password2:
        print("password not same")

    email = input("admin email: ")

    try:
        email = validate_email(email, check_deliverability=False)
        email = email.normalized
    except EmailNotValidError as e:
        print(str(e))
    else:
        try:
            user = User(username, email, password, role="admin").add()
        except IntegrityError as e:
            print(e)
        else:
            print("admin created")
