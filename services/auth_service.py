from repositories.user_repository import UserRepository
from utils.security import hash_password


class AuthService:

    @staticmethod
    def login_user(email, password):
        user = UserRepository.get_user_by_email(email)

        if not user:
            return False, "User not found", None

        password_hash = hash_password(password)

        if user["PASSWORD_HASH"] != password_hash:
            return False, "Incorrect password", None

        if user["ESTADO_CUENTA"] != "ACTIVO":
            return False, "Inactive account", None

        return True, "Login successful", user

    @staticmethod
    def register_user(user_data):
        existing_user = UserRepository.get_user_by_email(user_data["correo"])

        if existing_user:
            return False, "Email is already registered"

        user_data["password_hash"] = hash_password(user_data["password"])
        return UserRepository.create_user(user_data)