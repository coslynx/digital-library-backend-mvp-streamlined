from sqlalchemy.orm import Session

from src.domain.users.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        """
        Creates a new user in the database.

        Args:
            user: User object representing the user to be created.

        Returns:
            User: The newly created user object.
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by its ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            User: The retrieved user object, or None if not found.
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User:
        """
        Retrieves a user by its username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            User: The retrieved user object, or None if not found.
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        """
        Retrieves a user by its email.

        Args:
            email: The email of the user to retrieve.

        Returns:
            User: The retrieved user object, or None if not found.
        """
        return self.session.query(User).filter(User.email == email).first()

    def update(self, user_id: int, user: User) -> User:
        """
        Updates an existing user in the database.

        Args:
            user_id: The ID of the user to update.
            user: User object containing the updated user data.

        Returns:
            User: The updated user object.
        """
        db_user = self.session.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.username = user.username
            db_user.email = user.email
            db_user.password_hash = user.password_hash
            db_user.role = user.role
            db_user.is_active = user.is_active
            self.session.commit()
            self.session.refresh(db_user)
            return db_user
        else:
            return None

    def delete(self, user_id: int) -> bool:
        """
        Deletes a user from the database.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        else:
            return False