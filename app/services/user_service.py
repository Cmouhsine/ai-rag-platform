from app.auth.password import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate):

        existing_user = self.repository.get_by_email(
            user_data.email
        )

        if existing_user:
            raise ValueError("Email already exists.")

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
        )

        return self.repository.create(user)

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def get_users(self):
        return self.repository.list()

    def delete_user(self, user_id: int):

        user = self.repository.get_by_id(user_id)

        if not user:
            return None

        self.repository.delete(user)

        return user