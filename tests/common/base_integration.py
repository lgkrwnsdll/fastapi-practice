import unittest

from httpx import AsyncClient, ASGITransport

from app.config.db_config import inject_session
from app.main import app
from app.v2.entity import BaseEntity
from tests.config.db_config import test_engine, override_inject_session


class BaseIntegrationTestCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        app.dependency_overrides[inject_session] = override_inject_session
        cls.aclient = AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000")

        BaseEntity.metadata.create_all(test_engine)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

        BaseEntity.metadata.drop_all(test_engine)
        test_engine.dispose()
