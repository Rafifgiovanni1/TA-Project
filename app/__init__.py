from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData
from jinja2 import Template


app = Flask(__name__)

metadata = MetaData(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

login_manager = LoginManager()
db = SQLAlchemy(session_options={"autoflush": False},metadata=metadata)
migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    # load config
    from .config import Config

    app.config.from_object(Config)

    # login manager settings
    login_manager.login_view = "authentication.login"
    login_manager.login_message = "Mohon login terlebih dahulu"
    login_manager.login_message_category = "danger"

    # init plugin
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db,compare_type=True,render_as_batch=True)
    csrf.init_app(app)

    # register blueprint
    from .controller.admin import admin
    from .controller.authentication import authentication
    # from .controller.student import student
    # from .controller.teacher import teacher

    from .utils.cli import create_admin

    app.cli.add_command(create_admin)

    app.register_blueprint(admin, url_prefix="/admin")
    # app.register_blueprint(student,url_prefix="/student")
    # app.register_blueprint(teacher,url_prefix="/teacher")
    app.register_blueprint(authentication)

    # load model
    from .model.user import User
    from .model.students import Student

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/guide")
    def guide():
        template = Template(open("app/readme.md","r").read()).render(url_for=url_for)
        template = markdown(template, extensions=["fenced_code","codehilite","tables","toc","pymdownx.magiclink"])
        style = HtmlFormatter(style="emacs",full=True,cssclass="codehilite").get_style_defs(".codehilite")

        return render_template("guide.html",template=template,style=f"<style>{style} pre{{padding: 1rem}} img{{width: 100%;box-shadow: 5rem;}} </style>")

    @app.template_filter()
    def to_dict_value(text: str, key):
        from json import loads

        return loads(text)[key]

    return app
