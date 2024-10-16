import pytest
from unittest.mock import patch

from src.domain.users.services.user_service import UserService
from src.domain.users.models.user import User
from src.utils.exceptions import UserNotFoundError, InvalidCredentialsError
from src.utils.jwt_utils import create_access_token, decode_token
from src.infrastructure.database.models.base import Base
from sqlalchemy.orm import Session
from fastapi import HTTPException

# Mock SQLAlchemy session
class MockSession:
    def __init__(self):
        self.added_objects = []

    def add(self, obj: Base):
        self.added_objects.append(obj)

    def commit(self):
        pass

    def refresh(self, obj: Base):
        pass

    def query(self, model):
        return self

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return None

@pytest.fixture
def mock_session():
    return MockSession()

@pytest.fixture
def user_service(mock_session):
    user_repository = UserRepository(session=mock_session)
    return UserService(user_repository=user_repository)

def test_register_user_success(user_service, mock_session):
    user = User(username="testuser", email="testuser@example.com", password="password123")
    registered_user = user_service.register_user(session=mock_session, user=user)
    assert registered_user.username == "testuser"
    assert registered_user.email == "testuser@example.com"
    assert mock_session.added_objects[0] == user

def test_register_user_username_exists(user_service, mock_session):
    user1 = User(username="testuser", email="testuser@example.com", password="password123")
    user_service.register_user(session=mock_session, user=user1)
    user2 = User(username="testuser", email="testuser2@example.com", password="password123")
    with pytest.raises(HTTPException) as exc:
        user_service.register_user(session=mock_session, user=user2)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Username already exists."

def test_register_user_email_exists(user_service, mock_session):
    user1 = User(username="testuser", email="testuser@example.com", password="password123")
    user_service.register_user(session=mock_session, user=user1)
    user2 = User(username="testuser2", email="testuser@example.com", password="password123")
    with pytest.raises(HTTPException) as exc:
        user_service.register_user(session=mock_session, user=user2)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already exists."

def test_login_user_success(user_service, mock_session):
    user = User(username="testuser", email="testuser@example.com", password="password123")
    mock_session.query(User).filter(User.username == "testuser").first = lambda: user
    login_response = user_service.login_user(session=mock_session, username="testuser", password="password123")
    assert login_response.get("access_token") is not None

def test_login_user_invalid_credentials(user_service, mock_session):
    user = User(username="testuser", email="testuser@example.com", password="password123")
    mock_session.query(User).filter(User.username == "testuser").first = lambda: user
    with pytest.raises(InvalidCredentialsError) as exc:
        user_service.login_user(session=mock_session, username="testuser", password="wrongpassword")
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid credentials."

def test_login_user_user_not_found(user_service, mock_session):
    with pytest.raises(UserNotFoundError) as exc:
        user_service.login_user(session=mock_session, username="nonexistentuser", password="password123")
    assert exc.value.status_code == 404
    assert exc.value.detail == "User with username nonexistentuser not found."

def test_get_user_by_id_success(user_service, mock_session):
    user = User(id=1, username="testuser", email="testuser@example.com", password="password123")
    mock_session.query(User).filter(User.id == 1).first = lambda: user
    retrieved_user = user_service.get_user_by_id(session=mock_session, user_id=1)
    assert retrieved_user.id == 1
    assert retrieved_user.username == "testuser"

def test_get_user_by_id_not_found(user_service, mock_session):
    with pytest.raises(UserNotFoundError) as exc:
        user_service.get_user_by_id(session=mock_session, user_id=999)
    assert exc.value.status_code == 404
    assert exc.value.detail == "User with ID 999 not found."

def test_get_current_user_success(user_service, mock_session):
    user = User(username="testuser", email="testuser@example.com", password="password123", role="patron")
    mock_session.query(User).filter(User.username == "testuser").first = lambda: user
    token = create_access_token(data={"sub": "testuser", "role": "patron"})
    retrieved_user = user_service.get_current_user(session=mock_session, token=token)
    assert retrieved_user.username == "testuser"
    assert retrieved_user.role == "patron"

def test_get_current_user_invalid_token(user_service, mock_session):
    with patch("src.utils.jwt_utils.decode_token") as mock_decode_token:
        mock_decode_token.side_effect = Exception("Invalid token")
        with pytest.raises(HTTPException) as exc:
            user_service.get_current_user(session=mock_session, token="invalid_token")
        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid token."

def test_get_current_user_token_missing_username(user_service, mock_session):
    token = create_access_token(data={"role": "patron"})
    with pytest.raises(HTTPException) as exc:
        user_service.get_current_user(session=mock_session, token=token)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Token does not contain username."

def test_get_current_user_user_not_found(user_service, mock_session):
    token = create_access_token(data={"sub": "nonexistentuser", "role": "patron"})
    with pytest.raises(UserNotFoundError) as exc:
        user_service.get_current_user(session=mock_session, token=token)
    assert exc.value.status_code == 404
    assert exc.value.detail == "User with username nonexistentuser not found."

def test_get_current_user_unauthorized_role(user_service, mock_session):
    user = User(username="testuser", email="testuser@example.com", password="password123", role="staff")
    mock_session.query(User).filter(User.username == "testuser").first = lambda: user
    token = create_access_token(data={"sub": "testuser", "role": "patron"})
    with pytest.raises(HTTPException) as exc:
        user_service.get_current_user(session=mock_session, token=token)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Unauthorized."

def test_update_user_profile_success(user_service, mock_session):
    user = User(id=1, username="testuser", email="testuser@example.com", password="password123")
    mock_session.query(User).filter(User.id == 1).first = lambda: user
    updated_user = User(username="updateduser", email="updateduser@example.com", password="newpassword")
    updated_user = user_service.update_user_profile(session=mock_session, user_id=1, user=updated_user)
    assert updated_user.username == "updateduser"
    assert updated_user.email == "updateduser@example.com"

def test_update_user_profile_not_found(user_service, mock_session):
    with pytest.raises(UserNotFoundError) as exc:
        user_service.update_user_profile(session=mock_session, user_id=999, user=User())
    assert exc.value.status_code == 404
    assert exc.value.detail == "User with ID 999 not found."

def test_delete_user_success(user_service, mock_session):
    user = User(id=1, username="testuser", email="testuser@example.com", password="password123")
    mock_session.query(User).filter(User.id == 1).first = lambda: user
    deleted = user_service.delete_user(session=mock_session, user_id=1)
    assert deleted is True

def test_delete_user_not_found(user_service, mock_session):
    with pytest.raises(UserNotFoundError) as exc:
        user_service.delete_user(session=mock_session, user_id=999)
    assert exc.value.status_code == 404
    assert exc.value.detail == "User with ID 999 not found."