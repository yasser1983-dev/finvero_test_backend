from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None



class TaskCreate(TaskBase):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class TaskUpdateStatus(BaseModel):
    completed: bool


class TaskOut(TaskBase):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    creation_date: datetime