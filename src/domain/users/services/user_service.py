from typing import Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.domain.users.models.user import User
from src.domain.users.repositories.user_repository import UserRepository
from src.utils.exceptions import UserNotFoundError, InvalidCredentialsError
from src.utils.jwt_utils import create_access_token, decode_token

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, session: Session, user: User) -> User:
        """Registers a new user in the system.

        Args:
            session: SQLAlchemy session.
            user: User object containing the new user data.

        Returns:
            User: The newly created user object.

        Raises:
            HTTPException: If a user with the same username or email already exists.
        """
        existing_user = self.user_repository.get_by_username(session, user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists.")

        existing_user = self.user_repository.get_by_email(session, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists.")

        user.set_password(user.password)  # Hash the password before saving
        return self.user_repository.create(session, user)

    def login_user(self, session: Session, username: str, password: str) -> Dict[str, Any]:
        """Authenticates a user and returns an access token if successful.

        Args:
            session: SQLAlchemy session.
            username: The username of the user to authenticate.
            password: The password provided by the user.

        Returns:
            Dict[str, Any]: A dictionary containing the access token.

        Raises:
            InvalidCredentialsError: If the provided credentials are incorrect.
            UserNotFoundError: If no user is found with the given username.
        """
        user = self.user_repository.get_by_username(session, username)
        if not user:
            raise UserNotFoundError(f"User with username {username} not found.")

        if not user.check_password(password):
            raise InvalidCredentialsError("Invalid credentials.")

        access_token = create_access_token(data={"sub": user.username, "role": user.role})
        return {"access_token": access_token}

    def get_user_by_id(self, session: Session, user_id: int) -> User:
        """Retrieves a user by their ID.

        Args:
            session: SQLAlchemy session.
            user_id: The ID of the user to retrieve.

        Returns:
            User: The retrieved user object.

        Raises:
            UserNotFoundError: If no user is found with the given ID.
        """
        user = self.user_repository.get_by_id(session, user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        return user

    def get_current_user(self, session: Session, token: str) -> User:
        """Retrieves the current user based on the provided access token.

        Args:
            session: SQLAlchemy session.
            token: The access token provided by the client.

        Returns:
            User: The currently authenticated user object.

        Raises:
            HTTPException: If the token is invalid or expired.
            UserNotFoundError: If no user is found with the given username.
        """
        try:
            payload = decode_token(token)
            username = payload.get("sub")
            role = payload.get("role")

            if not username:
                raise HTTPException(status_code=401, detail="Token does not contain username.")

            user = self.user_repository.get_by_username(session, username)
            if not user:
                raise UserNotFoundError(f"User with username {username} not found.")

            if user.role != role:
                raise HTTPException(status_code=403, detail="Unauthorized.")

            return user

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token.")

    def update_user_profile(self, session: Session, user_id: int, user: User) -> User:
        """Updates the profile information of an existing user.

        Args:
            session: SQLAlchemy session.
            user_id: The ID of the user to update.
            user: User object containing the updated profile data.

        Returns:
            User: The updated user object.

        Raises:
            UserNotFoundError: If no user is found with the given ID.
        """
        updated_user = self.user_repository.update(session, user_id, user)
        if not updated_user:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        return updated_user

    def delete_user(self, session: Session, user_id: int) -> bool:
        """Deletes a user from the system.

        Args:
            session: SQLAlchemy session.
            user_id: The ID of the user to delete.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.

        Raises:
            UserNotFoundError: If no user is found with the given ID.
        """
        deleted = self.user_repository.delete(session, user_id)
        if not deleted:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        return deleted