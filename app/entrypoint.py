"""App manager file."""
from .factory import create_app, create_celery

app = create_app()
celery = create_celery()
