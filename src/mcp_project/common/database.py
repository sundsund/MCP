import os
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dispute_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def validate_provider_id(provider_id: str):
    """
    Validates that the provider_id is alphanumeric to prevent SQL injection.
    """
    if not re.match(r"^[a-zA-Z0-9_]+$", provider_id):
        raise ValueError("Invalid provider_id")

def get_db_session(provider_id: str):
    """
    Returns a database session with the search path set to the provider's schema.
    """
    validate_provider_id(provider_id)
    session = SessionLocal()
    schema_name = f"provider_{provider_id}"

    # Using text() with cautious interpolation after validation
    # Note: schema names cannot be bind parameters in PostgreSQL
    session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
    session.execute(text(f"SET search_path TO {schema_name}"))

    return session

def init_db():
    pass
