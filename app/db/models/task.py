from sqlalchemy import Column, Integer, String,ForeignKey,DateTime,Enum

from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy.sql import func
import uuid




class Task(Base):
    __tablename__ = "tasks"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(50), index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum("pending", "completed", name="status_enum"), default="pending", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    owner = relationship("User", back_populates="tasks")
