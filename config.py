from os import getenv

class Config:
  FLASK_APP = getenv('FLASK_APP')
  SECRET_KEY = getenv('SECRET_KEY')
  FLASK_ENV = getenv('FLASK_ENV')
  TESTING = getenv('TESTING', False)
