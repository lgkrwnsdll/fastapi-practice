import uuid

from app.v2.repository import ChildRepository, ParentRepository
from tests.common.base_repository import BaseRepositoryTestCase


class ChildRepositoryUnitTest(BaseRepositoryTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.child_repository = ChildRepository(db=self.session)
        self.parent_repository = ParentRepository(db=self.session)

    async def test_get_all_child_empty(self):
        result = await self.child_repository.get_all_child()
        self.assertEqual(len(result), 0)

    async def test_create_child_and_verify(self):
        # 생성
        await self.parent_repository.create_parent(uuid.uuid4().hex)
        await self.child_repository.create_child(uuid.uuid4().hex)
        await self.session.commit()  # 세이브포인트 커밋

        # 검증
        result = await self.child_repository.get_all_child()
        self.assertEqual(len(result), 1)


class ParentRepositoryUnitTest(BaseRepositoryTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.parent_repository = ParentRepository(db=self.session)

    async def test_get_all_parent_empty(self):
        result = await self.parent_repository.get_all_parent()
        self.assertEqual(len(result), 0)
