import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('CUPLOG_DATABASE_URL') or default_database_location
    SECRET_KEY = os.environ.get('CUPLOG_SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads') #directory to store uploaded photos