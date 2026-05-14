import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('CUPLOG_SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('CUPLOG_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    WTF_CSRF_ENABLED = False