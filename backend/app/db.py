import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Injected by the environment (GitHub secret -> .env on the VM -> container env)
DATABASE_URL = os.environ["DATABASE_URL"]

# Small pool: PostgreSQL B1ms allows only ~50 connections in total
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=5)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session():
    with SessionLocal() as session:
        yield session
