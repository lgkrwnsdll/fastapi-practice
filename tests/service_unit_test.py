import unittest
from unittest.mock import AsyncMock

from app.config.db_config import session_context
from app.v2.entity import Child, Parent
from app.v2.repository import ChildRepository, ParentRepository
from app.v2.service import Service


class ServiceUnitTest(unittest.IsolatedAsyncioTestCase):
    session_context.set(AsyncMock())  # Transactional 무효화

    async def asyncSetUp(self):
        """테스트마다 고유한 목 객체 제공해야 독립적인 수행 가능"""
        self.mock_child_repo = AsyncMock(ChildRepository)
        self.mock_parent_repo = AsyncMock(ParentRepository)

        self.service = Service(
            child_repository=self.mock_child_repo,
            parent_repository=self.mock_parent_repo
        )

    async def test_get_data_success(self):
        child_list = [Child()]
        parent_list = [Parent()]

        self.mock_child_repo.get_all_child.return_value = child_list
        self.mock_parent_repo.get_all_parent.return_value = parent_list

        result = await self.service.get_data()

        self.assertEqual(result, child_list + parent_list)

        self.mock_child_repo.get_all_child.assert_awaited_once()
        self.mock_parent_repo.get_all_parent.assert_awaited_once()

        self.mock_child_repo.get_all_child.assert_called_once()
        self.mock_parent_repo.get_all_parent.assert_called_once()

    async def test_create_data_success(self):
        child_list = []
        parent_list = []

        self.mock_child_repo.get_all_child.return_value = child_list
        self.mock_parent_repo.get_all_parent.return_value = parent_list

        result = await self.service.create_data()

        self.assertEqual(result, child_list + parent_list)
