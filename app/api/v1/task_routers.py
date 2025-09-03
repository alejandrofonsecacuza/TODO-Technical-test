from typing import List
from fastapi import APIRouter, Depends, status,Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import task as task_schema
from app.dependens.db import get_db
from app.dependens.security import get_current_user
from app.schemas.user import UserOut

from app.services.task_service import TaskService

router = APIRouter()

@router.post("/", response_model=task_schema.Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: task_schema.TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await TaskService(db).create_user_task(task=task, user_id=current_user.id)

@router.get("/", response_model=List[task_schema.Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await TaskService(db).get_tasks(user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=task_schema.Task)
async def read_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await TaskService(db).get_task(task_id=task_id,user_id=current_user.id)

@router.put("/{task_id}", response_model=task_schema.Task)
async def update_task(
    task_id: str,
    task: task_schema.TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    
    return await TaskService(db).update_task(task_id=task_id, user_id=current_user.id, task_update=task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    await TaskService(db).delete_task(task_id=task_id,user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)