import asyncio
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.repositories import InMemoryTaskRepository, TaskRepository


# Usa la implementación en memoria para tests (independiente de Mongo)


async def _test_repo_dep():
    return InMemoryTaskRepository()


app.dependency_overrides[TaskRepository] = _test_repo_dep
client = TestClient(app)


def test_create_and_list_tasks():
    res = client.post("/tasks/", json={"title": "Primera", "description": "demo"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Primera"
    assert data["completed"] is False


    res = client.get("/tasks/")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1


def test_update_and_delete():
    # crear
    res = client.post("/tasks/", json={"title": "X"})
    tid = res.json()["id"]

    # marcar completada
    res = client.p