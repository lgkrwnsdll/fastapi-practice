from typing import Sequence

from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db_config import inject_session
from app.v2.abstract_repository import AbstractChildRepository
from app.v2.entity import Child, Parent


class ChildRepository(AbstractChildRepository):

    async def get_all_child(self) -> Sequence[Child]:
        result = await self.db.execute(select(Child))
        return result.scalars().all()

    async def create_child(self, name: str) -> None:
        result = await self.db.execute(insert(Child).values(name=name))


class ParentRepository:
    def __init__(self, db: AsyncSession = Depends(inject_session)):
        print("=================================parent repo init=================================")
        self.db = db

    async def get_all_parent(self) -> Sequence[Parent]:
        result = await self.db.execute(select(Parent))
        return result.scalars().all()

    async def create_parent(self, name: str) -> None:
        result = await self.db.execute(insert(Parent).values(name=name))
