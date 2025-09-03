# Imports
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# Schemas
from app.schemas import task as task_schema

# Models
from app.db.models.task import Task as TaskModel

#Core
from app.core.log import logger

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_task(self, task_id: int, user_id: int):
        """Obtiene una tarea específica por su ID."""
        try:
            result = await self.db.execute(
                select(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user_id)
            )
            task = result.scalars().first()
            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except SQLAlchemyError as e:
            logger.error(f"Error fetching task {task_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")

    async def get_tasks(self, user_id: int, skip: int = 0, limit: int = 100):
        """Obtiene una lista paginada de tareas para un usuario específico."""
        try:
            result = await self.db.execute(
                select(TaskModel)
                .filter(TaskModel.user_id == user_id)
                .offset(skip)
                .limit(limit)
            )
            tasks = result.scalars().all()
            logger.info(f"Fetched {len(tasks)} tasks for user {user_id}")
            return tasks
        except SQLAlchemyError as e:
            logger.error(f"Error fetching tasks for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")

    async def create_user_task(self, task: task_schema.TaskCreate, user_id: int):
        """Crea una nueva tarea asociada a un usuario."""
        try:
            db_task = TaskModel(**task.model_dump(), user_id=user_id)
            self.db.add(db_task)
            await self.db.commit()
            await self.db.refresh(db_task)
            logger.info(f"Task {db_task.id} created for user {user_id}")
            return db_task
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error creating task for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")

    async def update_task(self, task_id: int, user_id: int, task_update: task_schema.TaskUpdate):
        """Actualiza los datos de una tarea existente."""
        try:
            db_task = await self.get_task(task_id, user_id)
            update_data = task_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            await self.db.commit()
            await self.db.refresh(db_task)
            logger.info(f"Task {task_id} updated for user {user_id}")
            return db_task
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error updating task {task_id} for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")

    async def delete_task(self, task_id: int, user_id: int):
        """Elimina una tarea de la base de datos."""
        try:
            db_task = await self.get_task(task_id, user_id)
            await self.db.delete(db_task)
            await self.db.commit()
            logger.info(f"Task {task_id} deleted for user {user_id}")
            return db_task
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error deleting task {task_id} for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")
