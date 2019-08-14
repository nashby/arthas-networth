import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL')

    BASIC_AUTH_USERNAME = os.environ.get('AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('AUTH_PASSWORD')
