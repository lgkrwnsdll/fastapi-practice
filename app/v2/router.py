from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from app.v2.service import Service

v2_router = APIRouter(prefix="/v2", tags=["v2"])


@cbv(v2_router)
class Router:
    def __init__(self, service: Service = Depends()):
        print("=================================v2_router init=================================")
        self.service = service

    @v2_router.get("/data")
    async def get_data(self):
        response = await self.service.get_data()
        return response

    @v2_router.post("/data", status_code=status.HTTP_201_CREATED)
    async def create_data(self):
        response = await self.service.create_data()
        return response
