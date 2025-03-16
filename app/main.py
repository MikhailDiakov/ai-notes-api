from fastapi import FastAPI
from .routers import notes, analytics
from .database import engine, Base

app = FastAPI(title="AI-Enhanced Notes Management System")

Base.metadata.create_all(bind=engine)

app.include_router(notes.router, prefix="/notes", tags=["Notes"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
