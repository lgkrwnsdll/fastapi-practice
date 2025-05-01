import unittest

from httpx import AsyncClient, ASGITransport

from app.main import app


class BaseRouterTestCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.aclient = AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000")

    async def asyncTearDown(self):
        app.dependency_overrides.clear()
