from os import getenv
import redis

class Config:
  FLASK_APP = getenv('FLASK_APP')
  SECRET_KEY = getenv('SECRET_KEY')
  URL = getenv('URL')
  
  FLASK_ENV = getenv('FLASK_ENV')
  TESTING = getenv('TESTING', False)
  DEBUG = getenv('DEBUG')

  SESSION_TYPE = getenv('SESSION_TYPE')
  SESSION_REDIS = redis.from_url(getenv('REDIS_URL'))
  
  DROPBOX_APP_KEY = getenv('DROPBOX_APP_KEY')
  DROPBOX_APP_SECRET = getenv('DROPBOX_APP_SECRET')
  