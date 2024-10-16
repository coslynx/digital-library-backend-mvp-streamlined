from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.domain.users.models.user import User
from src.domain.users.services.user_service import UserService
from src.utils.exceptions import UserNotFoundError, InvalidCredentialsError
from src.utils.jwt_utils import create_access_token
from src.infrastructure.api.dependencies.database import get_db
from src.config.settings import settings

from src.infrastructure.api.v1.schemas.auth import Token, UserCreate, UserLogin


class UsersController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register_user(self, user: UserCreate, db: Session = Depends(get_db)):
        """Registers a new user in the system."""
        try:
            new_user = self.user_service.register_user(db, user)
            return new_user
        except HTTPException as e:
            raise e

    async def login_user(self, user: UserLogin, db: Session = Depends(get_db)):
        """Authenticates a user and returns an access token if successful."""
        try:
            user = self.user_service.login_user(db, user.username, user.password)
            access_token = create_access_token(
                data={"sub": user.username, "role": user.role}
            )
            return {"access_token": access_token, "token_type": "bearer"}
        except UserNotFoundError as e:
            raise HTTPException(
                status_code=401,
                detail=f"User with username {user.username} not found.",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
        except InvalidCredentialsError as e:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e


def get_users_controller(user_service: UserService = Depends()):
    """Provides the UsersController instance as a FastAPI dependency."""
    return UsersController(user_service)