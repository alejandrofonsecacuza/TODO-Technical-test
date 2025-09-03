from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tasks = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete"  # Si el usuario es eliminado pues también sus tareas serán eliminadas----
    )