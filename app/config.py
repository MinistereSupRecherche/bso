"""Flask config file."""
import os
from app.api.eve import EVE_DOMAINS


class BaseConfig:
    """Base configuration."""

    DEBUG = False
    TESTING = False

    # Env required
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    SECRET_KEY = os.getenv("FLASK_SECRET")

    APP_NAME = os.getenv("APP_NAME") or 'publications'
    APP_SETTINGS = os.getenv("APP_SETTINGS") or "app.config.ProductionConfig"
    DATETIME_FORMAT = os.getenv("DATETIME_FORMAT") or "%Y-%m-%dT%H:%M:%S"
    LOGGER_DATE_FORMAT = os.getenv("LOGGER_DATE_FORMAT") \
        or "%Y-%m-%d %H:%M:%S %z"
    DATETIME_FORMAT_SCANR = os.getenv("DATETIME_FORMAT_SCANR") or "%4Y-%m-%d"

    LOGGER_FORMAT = os.getenv("LOGGER_FORMAT") or \
        "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s"

    # Mongo
    MONGO_HOST = os.getenv("MONGO_HOST") or "mongodb://mongo"
    MONGO_PORT = os.getenv("MONGO_PORT") or "27017"
    MONGO_URI = f"{MONGO_HOST}:{int(MONGO_PORT)}"
    MONGO_DBNAME = os.getenv("MONGO_DBNAME") or APP_NAME

    # Celery
    CELERY_BROKER_URI = os.getenv("CELERY_BROKER_URI") \
        or "redis://redis:6379/4"
    CELERY_TASK_LOGGER_FORMAT = os.getenv("LOGGER_FORMAT") or \
        "[%(asctime)s] [%(processName)s] [%(levelname)s] " +\
        "[%(name)s] [%(task_name)s::%(task_id)s] %(message)s"

    # self
    MAIN_COLLECTION_NAME = os.getenv("MAIN_COLLECTION_NAME") or APP_NAME
    SCANR_COLLECTION_NAME = os.getenv("SCANR_COLLECTION_NAME") or 'scanr'
    TASKS_COLLECTION_NAME = (
        os.getenv("TASKS_COLLECTION_NAME") or 'tasks')

    # Dependancies
    SELF_URL = "http://localhost:5000/"
    DATAESR_PUBLICATIONS_URL = SELF_URL + "publications/publications"
    DATAESR_NOTICES_PUBLICATIONS_URL = SELF_URL + "publications/notices_publications"
    HAL_URL_AUTHOR = "https://api.archives-ouvertes.fr/ref/author/"
    HAL_URL_STRUCTURE = "https://api.archives-ouvertes.fr/ref/structure/"
    HAL_URL_DOMAIN = "https://api.archives-ouvertes.fr/ref/domain/"

    # Ftp
    FTP_HOST = os.getenv("FTP_HOST")
    FTP_USER = os.getenv("FTP_USER")
    FTP_PASSWORD = os.getenv("FTP_PASSWORD")
    FTP_SCANR_PREPROD_DIR = os.getenv("FTP_SCANR_PREPROD_DIR")
    FTP_SCANR_PROD_DIR = os.getenv("FTP_SCANR_PROD_DIR")

    # Global prefixes for APIs
    URL_PREFIX = APP_NAME

    # Global ressource methods
    RESOURCE_METHODS = ['GET', 'POST']
    ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

    # API generated document keys renaming without heading underscore
    ITEMS = 'data'
    LINKS = 'hrefs'
    META = 'meta'
    ETAG = 'etag'
    ERROR = 'error'
    ISSUES = 'issues'
    STATUS = 'status'
    ITEM_URL = 'regex(".*")'

    # Primary key default
    ID_FIELD = "id"
    ITEM_LOOKUP_FIELD = "id"

    # Pagination params
    PAGINATION_DEFAULT = 20
    PAGINATION_LIMIT = 1000

    DATE_FORMAT = DATETIME_FORMAT
    LAST_UPDATED = 'modified_at'
    DATE_CREATED = 'created_at'

    MONGO_QUERY_BLACKLIST = ['$where']
    # Cross domain configurations
    X_DOMAINS = ['*']
    X_HEADERS = ['Content-Type', 'If-Match']

    # Do not produce application/XML
    RENDERERS = ['eve.render.JSONRenderer']

    # Domains définition {ressource_name: definition_reference}
    DOMAIN = EVE_DOMAINS


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    MONGO_DBNAME = BaseConfig.MONGO_DBNAME + "-dev"
    CELERY_RESULT_URI = f"{BaseConfig.MONGO_URI}/{MONGO_DBNAME}"


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    MONGO_DBNAME = f"{BaseConfig.MONGO_DBNAME}-test"
    CELERY_RESULT_URI = (
        f"{BaseConfig.MONGO_URI}/{MONGO_DBNAME}")


class ProductionConfig(BaseConfig):
    """Production configuration."""

    CELERY_RESULT_URI = f"{BaseConfig.MONGO_URI}/{BaseConfig.MONGO_DBNAME}"
