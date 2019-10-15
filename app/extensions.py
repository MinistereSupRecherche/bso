"""Extentions."""
from flask_restplus import Api
from celery import Celery

# Instanciate celery and finilaze it in factory
celery = Celery(__name__, autofinalize=False)

# RestPlus instances
rp = Api(
    version='1',
    doc="/doc",
    title='Publications API',
    description='Service aimed at managing publications in dataesr',
    validate=True)
