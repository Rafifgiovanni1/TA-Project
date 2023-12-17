from os import environ
from distutils.util import strtobool
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


class Config(object):
    DEBUG = strtobool(environ.get("DEBUG"))
    ENV = environ.get("ENV")

    DBASE_NAME =  environ.get("DBASE_NAME")
    DBASE_USERNAME =  environ.get("DBASE_USERNAME")
    # DBASE_PASSWORD =  quote_plus(environ.get("DBASE_PASSWORD"))
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DBASE_USERNAME}:{DBASE_PASSWORD}@localhost/{DBASE_NAME}" if DBASE_PASSWORD else "mysql+pymysql://{DBASE_USERNAME}@localhost/{DBASE_NAME}"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dbase.db"

    SECRET_KEY = environ.get("SECRET_KEY")
