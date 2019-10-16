"""App factory file."""
from eve import Eve
from flask_cors import CORS
from flask import Blueprint, Config
from eve_swagger import swagger

from .config import BaseConfig
from .extensions import celery, rp

from .api.eve.validators import CustomValidator
from .api.eve.swagger import swagger_info
from .api.custom.routes import analyzer

from .utils.celery import configure_celery
from .utils.logger import configure_logger, create_logger
from .utils.json_encoding import CustomJSONEncoder


logger = create_logger(__name__)


def create_app():
    """Create Flask app."""
    return entrypoint(mode='flask')


def create_celery():
    """Create celery workers."""
    return entrypoint(mode='celery')


def entrypoint(mode="flask"):
    """Application factory."""
    assert isinstance(mode, str), f"bad mode type '{type(mode)}'"
    assert mode in ('flask', 'celery'), f"bad mode '{mode}'"
    logger.info(
        f"Configuring {BaseConfig.APP_NAME} application with {mode} mode")

    logger.info("Configuring flask...")
    # Create a Flask Config object from APP_SETTINGS
    app_settings = BaseConfig.APP_SETTINGS
    config = Config('')
    config.from_object(app_settings)
    app = Eve(settings=config, validator=CustomValidator)
    CORS(app)

    # Finalize celery configuration
    configure_celery(app, celery)

    # Custom flask encoders
    app.json_encoder = CustomJSONEncoder

    # Set restplus custom routes blueprint
    bp = Blueprint('bp', __name__, url_prefix=f"/{BaseConfig.APP_NAME}")
    rp.init_app(bp)
    # rp.namespaces.clear()
    rp.add_namespace(analyzer)

    # Register custom routes Blueprint
    app.register_blueprint(bp)
    app.register_blueprint(swagger)
    app.config["SWAGGER_INFO"] = swagger_info
    app.logger = configure_logger(app.logger)

    # setting models attribute to flask
    setattr(app, "models", {})

    if mode == "flask":
        logger.info("Flask configuration successful!")
        return app
    if mode == "celery":
        logger.info("Celery configuration successful!")
        return celery
