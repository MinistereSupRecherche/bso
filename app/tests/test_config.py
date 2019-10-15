"""Config tester."""
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app.entrypoint import app, celery

if app.config["MODE"] == "DEV":
    class TestDevelopmentConfig(TestCase):
        """Tests for celery and flask configs for Dev, Prod and Test."""

        def create_app(self):
            """Set APP_SETTINGS."""
            app.config.from_object('app.config.DevelopmentConfig')
            return app

        def test_app_is_dev(self):
            """Test flask config object in dev mode."""
            self.assertTrue(
                app.config["SECRET_KEY"] == os.getenv("FLASK_SECRET"))
            self.assertFalse(current_app is None)
            self.assertTrue(
                app.config["MONGO_URI"] == os.getenv("MONGO_HOST") + ":"
                + os.getenv("MONGO_PORT")
            )
            self.assertTrue(
                app.config["MONGO_DBNAME"] == f"{os.getenv('MONGO_DBNAME')}-dev"
            )
            self.assertTrue(app.config["DEBUG"])

        def test_celery_is_dev(self):
            """Test celery config object in dev mode."""
            URI = f"{os.getenv('MONGO_HOST')}:{int(os.getenv('MONGO_PORT'))}"
            URI += f"/{os.getenv('MONGO_DBNAME')}-dev"
            self.assertTrue(
                celery.conf.broker_url == os.getenv('CELERY_BROKER_URI'))
            self.assertTrue(
                celery.conf.result_backend == URI)
            self.assertTrue(
                celery.conf.worker_log_format == os.getenv('LOGGER_FORMAT'))
            self.assertTrue(
                celery.conf.worker_task_log_format == os.getenv(
                    'CELERY_TASK_LOGGER_FORMAT'))


if app.config["MODE"] == "TEST":
    class TestTestingConfig(TestCase):
        """Tests for celery and flask configs for Dev, Prod and Test."""

        def create_app(self):
            """Set APP_SETTINGS."""
            app.config.from_object('app.config.TestingConfig')
            return app

        def test_app_is_test(self):
            """Test flask config object in test mode."""
            self.assertTrue(
                app.config["SECRET_KEY"] == os.getenv("FLASK_SECRET"))
            self.assertFalse(current_app is None)
            self.assertTrue(
                app.config["MONGO_URI"] == os.getenv("MONGO_HOST") + ":"
                + os.getenv("MONGO_PORT")
            )
            self.assertTrue(
                app.config["MONGO_DBNAME"] == f"{os.getenv('MONGO_DBNAME')}-test"
            )
            self.assertFalse(app.config["DEBUG"])

        def test_celery_is_test(self):
            """Test celery config object in test mode."""
            URI = f"{os.getenv('MONGO_HOST')}:{int(os.getenv('MONGO_PORT'))}"
            URI += f"/{os.getenv('MONGO_DBNAME')}-test"
            self.assertTrue(
                celery.conf.broker_url == os.getenv('CELERY_BROKER_URI'))
            self.assertTrue(
                celery.conf.result_backend == URI)
            self.assertTrue(
                celery.conf.worker_log_format == os.getenv('LOGGER_FORMAT'))
            self.assertTrue(
                celery.conf.worker_task_log_format == os.getenv(
                    'CELERY_TASK_LOGGER_FORMAT'))


if app.config["MODE"] == "PROD":
    class TestProductionConfig(TestCase):
        """Tests for celery and flask configs for Dev, Prod and Test."""

        def create_app(self):
            """Set APP_SETTINGS."""
            app.config.from_object('app.config.DevelopmentConfig')
            return app

        def test_app_is_prod(self):
            """Test flask config object in production mode."""
            self.assertTrue(
                app.config["SECRET_KEY"] == os.getenv("FLASK_SECRET"))
            self.assertFalse(current_app is None)
            self.assertTrue(
                app.config["MONGO_URI"] == os.getenv("MONGO_HOST") + ":"
                + os.getenv("MONGO_PORT")
            )
            self.assertTrue(
                app.config["MONGO_DBNAME"] == os.getenv('MONGO_DBNAME'))
            self.assertFalse(app.config["DEBUG"])

        def test_celery_is_prod(self):
            """Test celery config object in production mode."""
            URI = f"{os.getenv('MONGO_HOST')}:{int(os.getenv('MONGO_PORT'))}"
            URI += f"/{os.getenv('MONGO_DBNAME')}"
            self.assertTrue(
                celery.conf.broker_url == os.getenv('CELERY_BROKER_URI'))
            self.assertTrue(
                celery.conf.result_backend == URI)
            self.assertTrue(
                celery.conf.worker_log_format == os.getenv('LOGGER_FORMAT'))
            self.assertTrue(
                celery.conf.worker_task_log_format == os.getenv(
                    'CELERY_TASK_LOGGER_FORMAT'))


if __name__ == "__main__":
    unittest.main()
