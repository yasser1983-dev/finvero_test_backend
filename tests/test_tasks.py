from fastapi.testclient import TestClient
from app.main import app
from app.repositories import InMemoryTaskRepository, TaskRepository

# Repo compartido en memoria
_test_repo = InMemoryTaskRepository()

def _test_repo_dep():
    return _test_repo

# Override para usar el repo en memoria
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
    assert res.status_code == 201
    tid = res.json()["id"]

    # marcar completada
    res = client.put(f"/tasks/{tid}", json={"completed": True})
    assert res.status_code == 200
    updated = res.json()
    assert updated["completed"] is True

    # eliminar
    res = client.delete(f"/tasks/{tid}")
    assert res.status_code == 204

    # verificar que ya no exista
    res = client.get("/tasks/")
    items = res.json()
    assert all(item["id"] != tid for item in items)
