import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from .db import Base, engine, get_session
from .models import Note
from .schemas import NoteIn, NoteOut

APP_VERSION = os.getenv("APP_VERSION", "dev")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lab shortcut: create tables on startup (enterprise: Alembic migrations)
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="FastAPI Azure Demo",
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)


@app.get("/api/health")
def health(session: Session = Depends(get_session)):
    # Touch the DB so "healthy" means "can actually serve requests"
    session.execute(text("SELECT 1"))
    return {"status": "ok", "version": APP_VERSION}


@app.get("/api/notes", response_model=list[NoteOut])
def list_notes(session: Session = Depends(get_session)):
    return session.scalars(select(Note).order_by(Note.id.desc()).limit(50)).all()


@app.post("/api/notes", response_model=NoteOut, status_code=201)
def create_note(payload: NoteIn, session: Session = Depends(get_session)):
    note = Note(text=payload.text)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note
