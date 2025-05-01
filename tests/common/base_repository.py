import unittest

from sqlalchemy.ext.asyncio import AsyncSession

from app.v2.entity import BaseEntity
from tests.config.db_config import test_async_engine, test_engine


class BaseRepositoryTestCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        BaseEntity.metadata.create_all(test_engine)

    @classmethod
    def tearDownClass(cls):
        BaseEntity.metadata.drop_all(test_engine)
        test_engine.dispose()

    async def asyncSetUp(self):
        self.async_engine = test_async_engine
        self.connection = await self.async_engine.connect()

        self.root_transaction = await self.connection.begin()

        self.session = AsyncSession(
            bind=self.connection,
            join_transaction_mode="create_savepoint"
        )

    async def asyncTearDown(self):
        await self.session.close()

        await self.root_transaction.rollback()

        await self.connection.close()
