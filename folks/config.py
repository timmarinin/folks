import os
from dotenv import load_dotenv
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key-should-be-long'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_BUCKET = 'folks-pim'
    S3_KEY = os.environ.get('FOLKS_S3_ACCESS_KEY')
    S3_SECRET = os.environ.get('FOLKS_S3_SECRET_ACCESS_KEY')
    S3_LOCATION = "https://{}.fra1.digitaloceanspaces.com/".format(S3_BUCKET)
    S3_ENDPOINT = 'fra1.digitaloceanspaces.com'
    CELERY_BROKER = os.environ.get('CELERY_BROKER')