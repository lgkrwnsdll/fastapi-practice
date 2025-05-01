from fastapi import FastAPI

from app.v2.router import v2_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(v2_router)
