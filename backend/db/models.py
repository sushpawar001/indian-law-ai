from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid

from .postgre_db import Base
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum


class ThreadMessageRole(str, Enum):
    ai = "ai"
    user = "user"
    system = "system"


# class ChatThread(BaseModel): # threads table
#     # user_id: str
#     thread_id: str # UUID


# class ThreadMessage(BaseModel): # messages table
#     thread_id: str # UUID
#     message_role: ThreadMessageRole
#     content: str
#     sent_at: datetime


class ChatThread(Base):
    __tablename__ = "threads"

    thread_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    messages = relationship(
        "ThreadMessage", back_populates="thread", cascade="all, delete"
    )


class ThreadMessage(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    thread_id = Column(
        UUID(as_uuid=True), ForeignKey("threads.thread_id"), nullable=False
    )

    message_role = Column(String, nullable=False)

    content = Column(String, nullable=False)

    sent_at = Column(DateTime, default=datetime.utcnow)

    thread = relationship("ChatThread", back_populates="messages")
