import pytest
from fastapi.testclient import TestClient

# Fixtures de conftest.py
# client y test_user_data ya están disponibles


@pytest.fixture
def test_user_data():
    """Fixture que proporciona datos de usuario de prueba."""
    return {
        "email": "test@example.com",
        "password": "strongpassword123"
    }

@pytest.fixture
def auth_headers(client: TestClient, test_user_data):
    """
    Registra y loguea al usuario de prueba, devuelve headers con token.
    """
    # Registramos al usuario
    client.post("/users/register", json=test_user_data)
    # Login
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/users/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def task_data():
    """
    Datos de ejemplo para crear tareas.
    """
    return {
        "title": "Tarea de prueba",
        "description": "Esta es una tarea de prueba",
    }

# ---------------------------
# Tests de Tasks
# ---------------------------

def test_create_task(client: TestClient, auth_headers, task_data):
    response = client.post("/tasks/", json=task_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert "id" in data

def test_read_tasks(client: TestClient, auth_headers, task_data):
    # Crear 2 tareas
    client.post("/tasks/", json=task_data, headers=auth_headers)
    client.post("/tasks/", json={**task_data, "title": "Otra tarea"}, headers=auth_headers)
    
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    titles = [task["title"] for task in data]
    assert "Tarea de prueba" in titles
    assert "Otra tarea" in titles

def test_read_single_task(client: TestClient, auth_headers, task_data):
    # Crear tarea
    create_resp = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_resp.json()["id"]

    # Leer tarea individual
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]

def test_update_task(client: TestClient, auth_headers, task_data):
    # Crear tarea
    create_resp = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_resp.json()["id"]

    # Actualizar tarea
    update_data = {"title": "Tarea actualizada", "description": "Descripción nueva"}
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]

def test_delete_task(client: TestClient, auth_headers, task_data):
    # Crear tarea
    create_resp = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_resp.json()["id"]

    # Borrar tarea
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verificar que ya no existe
    get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 404
