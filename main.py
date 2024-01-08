from fastapi import FastAPI
from db.engin import Base, engine
from routers.librarys import router as library_router

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(library_router, prefix="/author")

