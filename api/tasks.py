from celery import Celery
from config import Config

config = Config()
celeryApp = Celery('tasks', broker=config.REDIS_URL)


@celeryApp.task
def snipRecipes(recipeLinks):
    return "Snipping your recipes!"
