from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    ideas_requested = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="sessions")
    ideas = relationship("Idea", back_populates="session", cascade="all, delete-orphan")


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    rank = Column(Integer, nullable=True)
    total_score = Column(Float, nullable=True)
    score = Column(JSON, nullable=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    session = relationship("Session", back_populates="ideas")
    analysis = relationship("Analysis", back_populates="idea", uselist=False, cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    white = Column(Text, nullable=False)
    red = Column(Text, nullable=False)
    black = Column(Text, nullable=False)
    yellow = Column(Text, nullable=False)
    green = Column(Text, nullable=False)
    blue = Column(Text, nullable=False)
    idea_id = Column(Integer, ForeignKey("ideas.id"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    idea = relationship("Idea", back_populates="analysis")
