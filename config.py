import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_SECRET = 'SAJHF)HAw98heoahsokehI)ASHDF*Hgmsu9dhg'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///app'
    JWT_SECRET_KEY = 'super-secret'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
