"""
Database schema
"""

import dataclasses
import os

from dotenv import load_dotenv
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Text,
    create_engine,
    inspect,
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@dataclasses.dataclass
class Base(DeclarativeBase):
    """Base model for ORM classes"""


@dataclasses.dataclass
class Source(Base):
    """Dataset metadata"""

    __tablename__ = "source"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, index=True)
    url = Column(Text, nullable=False)

    # Relationship to URL table
    urls = relationship("URL", back_populates="source", cascade="all, delete")


@dataclasses.dataclass
class URL(Base):
    """URL data"""

    __tablename__ = "url"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("source.id", ondelete="CASCADE"), index=True)
    url = Column(Text, nullable=False, index=True)
    features = Column(JSON)
    is_phishing = Column(Boolean, nullable=False, index=True)
    is_online = Column(Boolean, default=False, index=True)

    # Relationship to Source table
    source = relationship("Source", back_populates="urls")


if __name__ == "__main__":
    # Create tables if they do not exist
    inspector = inspect(engine)

    if "source" in inspector.get_table_names() and "url" in inspector.get_table_names():
        print("Tables already exist.")
    else:
        print("Tables do not exist. Creating tables...")
        Base.metadata.create_all(engine)