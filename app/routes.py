from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import TaskCreate, TaskOut, TaskUpdateStatus
from app.repositories import TaskRepository


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskOut])
async def list_tasks(repo: TaskRepository = Depends()):
    return await repo.list_tasks()


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, repo: TaskRepository = Depends()):
    return await repo.create_task(payload)


@router.put("/{task_id}", response_model=TaskOut)
async def update_status(task_id: str, payload: TaskUpdateStatus, repo: TaskRepository = Depends()):
    updated = await repo.set_completed(task_id, payload.completed)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, repo: TaskRepository = Depends()):
    ok = await repo.delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None