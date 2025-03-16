from fastapi import FastAPI
from .routers import notes, analytics
from .database import engine, Base

app = FastAPI(title="AI-Enhanced Notes Management System")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(notes.router, prefix="/notes", tags=["Notes"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
