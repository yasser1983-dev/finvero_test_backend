from __future__ import annotations

from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.schemas import TaskOut, TaskCreate


class TaskRepository(ABC):
    @abstractmethod
    async def list_tasks(self) -> List[TaskOut]:
        ...

    @abstractmethod
    async def create_task(self, data: TaskCreate) -> TaskOut:
        ...

    @abstractmethod
    async def set_completed(self, task_id: str, completed: bool) -> Optional[TaskOut]:
        ...

    @abstractmethod
    async def delete_task(self, task_id: str) -> bool:
        ...


class MongoTaskRepository(TaskRepository):
    def __init__(self, coll: AsyncIOMotorCollection):
        self.coll = coll

    def _to_out(self, doc) -> TaskOut:
        return TaskOut(
            id=str(doc["_id"]),
            title=doc["title"],
            description=doc.get("description"),
            completed=doc.get("completed", False),
            creation_date=doc["creation_date"],
        )

    async def list_tasks(self) -> List[TaskOut]:
        cursor = self.coll.find({}, sort=[("creation_date", -1)])
        return [self._to_out(d) async for d in cursor]

    async def create_task(self, data: TaskCreate) -> TaskOut:
        doc = {
            "title": data.title,
            "description": data.description,
            "completed": False,
            "creation_date": datetime.utcnow(),
        }
        res = await self.coll.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._to_out(doc)

    async def set_completed(self, task_id: str, completed: bool) -> Optional[TaskOut]:
        try:
            oid = ObjectId(task_id)
        except Exception:
            return None
        res = await self.coll.find_one_and_update(
            {"_id": oid},
            {"$set": {"completed": completed}},
            return_document=True,
        )
        return self._to_out(res) if res else None

    async def delete_task(self, task_id: str) -> bool:
        try:
            oid = ObjectId(task_id)
        except Exception:
            return False
        res = await self.coll.delete_one({"_id": oid})
        return res.deleted_count == 1


async def set_completed(self, task_id: str, completed: bool) -> Optional[TaskOut]:
    try:
        oid = ObjectId(task_id)
    except Exception:
        return None
    res = await self.coll.find_one_and_update({"_id": oid}, {"$set": {"completed": completed}}, return_document=True)
    return self._to_out(res) if res else None


async def delete_task(self, task_id: str) -> bool:
    try:
        oid = ObjectId(task_id)
    except Exception:
        return False
    res = await self.coll.delete_one({"_id": oid})
    return res.deleted_count == 1


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._data: dict[str, dict] = {}

    def _to_out(self, doc) -> TaskOut:
        return TaskOut(
            id=str(doc["_id"]),
            title=doc["title"],
            description=doc.get("description"),
            completed=doc.get("completed", False),
            creation_date=doc["creation_date"],
        )

    async def list_tasks(self) -> List[TaskOut]:
        # ordenar por fecha de creación descendente
        docs = sorted(self._data.values(), key=lambda d: d["creation_date"], reverse=True)
        return [self._to_out(d) for d in docs]

    async def create_task(self, data: TaskCreate) -> TaskOut:
        oid = str(ObjectId())
        doc = {
            "_id": oid,
            "title": data.title,
            "description": data.description,
            "completed": False,
            "creation_date": datetime.now(),
        }
        self._data[oid] = doc
        return self._to_out(doc)

    async def set_completed(self, task_id: str, completed: bool) -> Optional[TaskOut]:
        doc = self._data.get(task_id)
        if not doc:
            return None
        doc["completed"] = completed
        return self._to_out(doc)

    async def delete_task(self, task_id: str) -> bool:
        return self._data.pop(task_id, None) is not None