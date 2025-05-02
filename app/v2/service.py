import uuid

from fastapi import Depends

from app.decorator import Transactional
from app.v2.abstract_repository import AbstractChildRepository, inject_child_repository
from app.v2.domain import ChildDomain, ParentDomain
from app.v2.repository import ParentRepository


class Service:
    def __init__(
            self,
            child_repository: AbstractChildRepository = Depends(inject_child_repository()),  # 인터페이스 의존
            parent_repository: ParentRepository = Depends()  # 구현체 의존
    ):
        print("=================================service init=================================")
        self.child_repository = child_repository
        self.parent_repository = parent_repository

    @Transactional(read_only=True)
    async def get_data(self) -> list:
        child_data = await self.child_repository.get_all_child()
        parent_data = await self.parent_repository.get_all_parent()

        # 커밋하지 않기 때문에 엔티티로 반환해도 데이터 누락 없음
        return child_data + parent_data

    @Transactional()
    async def create_data(self) -> list:
        await self.parent_repository.create_parent(uuid.uuid4().hex)
        await self.child_repository.create_child(uuid.uuid4().hex)

        child_data = await self.child_repository.get_all_child()
        parent_data = await self.parent_repository.get_all_parent()

        # 엔티티 반환 시 만료되어 데이터가 비어있다 -> expire_on_commit = True (디폴트)
        # expire_on_commit = False 적용 시 트랜잭션 종료 후 재접근 시 refresh 하지 않아 성능이 좋지만 정합성이 떨어질 수 있다
        return list(map(ChildDomain.from_entity, child_data)) + list(map(ParentDomain.from_entity, parent_data))
