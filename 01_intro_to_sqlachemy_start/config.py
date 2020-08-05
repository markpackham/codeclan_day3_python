import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHMEY_DATABASE_URL = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHMEY_TRACK_MODIFICATIONS = False