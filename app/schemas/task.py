
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

# Enum para status
class StatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"

# Propiedades base compartidas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

# Propiedades a recibir al crear una tarea
class TaskCreate(TaskBase):
    status: StatusEnum = StatusEnum.pending  # por defecto pending

# Propiedades a recibir al actualizar una tarea (todos los campos son opcionales)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None  # validación automática

# Propiedades a devolver al cliente (en la respuesta de la API)
class Task(TaskBase):
    id: str
    status: StatusEnum
    created_at: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)
