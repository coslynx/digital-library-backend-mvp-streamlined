import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime, timedelta

from src.config.settings import settings
from src.domain.users.models.user import User
from src.infrastructure.api.dependencies.database import get_db
from src.infrastructure.api.v1.controllers.auth_controller import AuthController
from src.domain.users.services.user_service import UserService
from src.domain.users.repositories.user_repository import UserRepository
from src.infrastructure.api.dependencies.auth import get_current_user
from src.utils.jwt_utils import decode_token
from src.utils.exceptions import UserNotFoundError, InvalidCredentialsError

from src.infrastructure.api.main import app

client = TestClient(app)
engine = create_engine(settings.DATABASE_URL)

@pytest.fixture(scope="module")
def db() -> Session:
    session = Session(engine)
    yield session
    session.close()

@pytest.fixture(scope="module")
def auth_controller(db: Session) -> AuthController:
    user_service = UserService(user_repository=UserRepository(session=db))
    yield AuthController(user_service=user_service)

@pytest.fixture(scope="module")
def user_data():
    yield {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
    }

def test_register_user(auth_controller: AuthController, db: Session, user_data):
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    user = db.query(User).filter_by(username=user_data["username"]).first()
    assert user is not None

def test_login_user_valid_credentials(auth_controller: AuthController, db: Session, user_data):
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    response = client.post("/api/v1/auth/token", data={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200
    assert response.json().get("access_token") is not None

def test_login_user_invalid_credentials(auth_controller: AuthController, db: Session, user_data):
    response = client.post("/api/v1/auth/token", data={"username": user_data["username"], "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Incorrect username or password"

def test_jwt_token_validation(auth_controller: AuthController, db: Session, user_data):
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    response = client.post("/api/v1/auth/token", data={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    payload = decode_token(access_token)
    assert payload.get("sub") == user_data["username"]
    assert payload.get("role") == "patron"

def test_get_current_user(auth_controller: AuthController, db: Session, user_data):
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    response = client.post("/api/v1/auth/token", data={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user["username"] == user_data["username"]
    assert retrieved_user["email"] == user_data["email"]

def test_get_current_user_invalid_token(auth_controller: AuthController, db: Session, user_data):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid authentication credentials"

def test_get_current_user_expired_token(auth_controller: AuthController, db: Session, user_data):
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    response = client.post("/api/v1/auth/token", data={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    payload = decode_token(access_token)
    payload["exp"] = datetime.utcnow() - timedelta(seconds=1)
    expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid authentication credentials"