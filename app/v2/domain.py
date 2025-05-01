from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.v2.entity import Parent, Child


class ChildDomain(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    @staticmethod
    def from_entity(child: Child) -> 'ChildDomain':
        return ChildDomain(id=child.id, name=child.name, parent_id=child.parent_id)


class ParentDomain(BaseModel):
    id: int
    name: str
    updated_at: Optional[datetime]

    @staticmethod
    def from_entity(parent: Parent) -> 'ParentDomain':
        return ParentDomain(id=parent.id, name=parent.name, updated_at=parent.updated_at)
