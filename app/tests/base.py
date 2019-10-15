# services/users/project/tests/base.py
from flask_testing import TestCase
from app.factory import create_app

app = create_app()


class BaseTestCase(TestCase):
    """Base test class."""

    def create_app(self):
        """Make configs for testing."""
        # app.config.from_object('app.config.TestingConfig')
        return app

    def tearDown(self):
        """Delete test datas."""
        app.data.driver.db.drop_collection("organizations")
