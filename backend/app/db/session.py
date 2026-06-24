from __future__ import annotations

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = getenv(
    "CAPAG_DATABASE_URL",
    "postgresql+psycopg://capag:capag_local_password@postgres:5432/capag",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

