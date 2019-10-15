"""Mongodb connexions providers."""
from functools import wraps
from pymongo import MongoClient
from flask import current_app as app
from ..config import BaseConfig


def get_mongo_dbname():
    """Get mongo dbname from config."""
    DBNAME = app.config["MONGO_DBNAME"]
    return DBNAME


def mongo_connect(f):
    """Decorate a function for mongo connexion."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        dbname = get_mongo_dbname()
        conn = MongoClient(BaseConfig.MONGO_URI)
        mongodb = conn[dbname]
        response = f(mongodb, *args, **kwargs)
        conn.close()
        return response
    return wrapper


def get_mongo(level="db"):
    """Get a mongodb connexion.

    Provides a mongo client if level is set to 'client'.
    Otherwise, it returns a connexion to the
    app configured 'MONGO_DBNAME' database
    """
    dbname = get_mongo_dbname()
    conn = MongoClient(BaseConfig.MONGO_URI)
    if level == 'client':
        return conn
    elif level == 'db':
        mongodb = conn[dbname]
        return mongodb
    else:
        raise Exception(
            "Unknown mongo level. Should be one of 'db' or 'client'")
