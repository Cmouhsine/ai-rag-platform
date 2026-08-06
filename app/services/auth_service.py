from app.auth.jwt import create_access_token
from app.auth.password import verify_password
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(
        self,
        email: str,
        password: str,
    ):

        user = self.repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return token