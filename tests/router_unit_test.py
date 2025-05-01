from unittest.mock import AsyncMock

from starlette import status

from app.main import app
from app.v2.service import Service
from tests.common.base_router import BaseRouterTestCase


class RouterUnitTest(BaseRouterTestCase):
    async def asyncSetUp(self):
        self.mock_service = AsyncMock(spec=Service)
        app.dependency_overrides[Service] = lambda: self.mock_service

    async def test_get_data(self):
        expected_response = []
        self.mock_service.get_data.return_value = expected_response

        resp = await self.aclient.get("/v2/data")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), expected_response)
        self.mock_service.get_data.assert_awaited_once()

    async def test_post_data(self):
        expected_response = []
        self.mock_service.create_data.return_value = expected_response

        resp = await self.aclient.post("/v2/data")

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json(), expected_response)
        self.mock_service.create_data.assert_awaited_once()