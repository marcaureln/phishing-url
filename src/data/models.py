"""
Database schema
"""

import dataclasses
import os

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    create_engine,
    inspect,
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy.sql import func

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, connect_args={"options": "-c timezone=utc"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@dataclasses.dataclass
class Base(DeclarativeBase):
    """Base model for ORM classes"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )


@dataclasses.dataclass
class Source(Base):
    """Dataset metadata"""

    __tablename__ = "source"

    name = Column(Text, nullable=False, unique=True)
    url = Column(Text, nullable=False, unique=True)

    # Relationship to URL table
    urls = relationship("URL", back_populates="source", cascade="all, delete")

    def __repr__(self):
        return f"<Source(id={self.id}, name={self.name}, url={self.url})>"


@dataclasses.dataclass
class URL(Base):
    """URL data"""

    __tablename__ = "url"

    source_id = Column(Integer, ForeignKey("source.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)
    is_phishing = Column(Boolean, nullable=False)
    is_online = Column(Boolean, default=False)

    # Relationship to Source table
    source = relationship("Source", back_populates="urls")

    def __repr__(self):
        return f"<URL(id={self.id}, source_id={self.source_id}, url={self.url}, is_phishing={self.is_phishing}, is_online={self.is_online})>"


if __name__ == "__main__":
    # Uncomment the following line to drop all tables
    # Base.metadata.drop_all(engine)
    # Create tables if they do not exist
    inspector = inspect(engine)

    if "source" in inspector.get_table_names() and "url" in inspector.get_table_names():
        print("Tables already exist.")
    else:
        print("Tables do not exist. Creating tables...")
        Base.metadata.create_all(engine)
