import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def test_user_data():
    """Fixture que proporciona datos de usuario de prueba."""
    return {
        "email": "test@example.com",
        "password": "strongpassword123"
    }

def test_register_user(client: TestClient, test_user_data):
    """
    Prueba el endpoint de registro de un nuevo usuario.
    Verifica que el usuario se crea correctamente y que los datos de la respuesta son los esperados.
    """
    response = client.post("/users/register", json=test_user_data)
    print(response.status_code)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == test_user_data["email"]

def test_register_existing_user(client: TestClient, test_user_data):
    """
    Prueba el caso en el que se intenta registrar un usuario que ya existe.
    Debe devolver un código de estado 409 (Conflict).
    """
    # Primero, registra al usuario
    client.post("/users/register", json=test_user_data)
    # Intenta registrarlo de nuevo
    response = client.post("/users/register", json=test_user_data)
    assert response.status_code == 409
    assert "Email already registered" == response.json()["detail"]

def test_login_user(client: TestClient, test_user_data):
    """
    Prueba el endpoint de inicio de sesión.
    Verifica que se puede iniciar sesión con éxito y se recibe un token.
    """
    # Primero, asegúrate de que el usuario está registrado
    client.post("/users/register", json=test_user_data)

    # Prepara los datos para el formulario de login
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }

    # Realiza la solicitud POST a /login
    response = client.post("/users/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient, test_user_data):
    """
    Prueba el inicio de sesión con credenciales incorrectas.
    Debe devolver un código de estado 401 (Unauthorized).
    """
    # Intenta iniciar sesión sin registrar el usuario o con credenciales erróneas
    login_data = {
        "username": "nonexist@entuser.com",
        "password": "wrongpassword"
    }
    response = client.post("/users/login", data=login_data)
    assert response.status_code == 401
    assert "Invalid credentials" == response.json()["detail"]

def test_get_profile_authenticated(client: TestClient, test_user_data):
    """
    Prueba el endpoint de perfil de usuario para un usuario autenticado.
    Verifica que se devuelve la información del usuario correcta.
    """
    # Primero, registra y loguea al usuario para obtener un token
    client.post("/users/register", json=test_user_data)
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    login_response = client.post("/users/login", data=login_data)
    access_token = login_response.json()["access_token"]

    # Realiza la solicitud GET a /me con el token en el encabezado de autorización
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]

def test_get_profile_unauthenticated(client: TestClient):
    """
    Prueba el endpoint de perfil de usuario sin autenticación.
    Debe devolver un código de estado 401 (Unauthorized).
    """
    response = client.get("/users/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]
