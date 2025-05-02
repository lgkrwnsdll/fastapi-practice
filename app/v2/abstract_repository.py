from abc import ABCMeta, abstractmethod

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db_config import inject_session


class AbstractChildRepository(metaclass=ABCMeta):
    def __init__(self, db: AsyncSession = Depends(inject_session)):
        print("=================================child repo init=================================")
        self.db = db

    @abstractmethod
    async def get_all_child(self):
        pass

    @abstractmethod
    async def create_child(self, name: str):
        pass


def inject_child_repository():
    from app.v2.repository import ChildRepository
    return ChildRepository
