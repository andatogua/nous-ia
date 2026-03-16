from repositories.profile_repository import ProfileRepository


class ProfileService:

    @staticmethod
    def get_profile(user_id):
        return ProfileRepository.get_user_profile(user_id)

    @staticmethod
    def update_profile(user_id, nombre, apellido, telefono, username):
        if not nombre.strip():
            return False, "El nombre es obligatorio."

        if not apellido.strip():
            return False, "El apellido es obligatorio."

        if not telefono.strip():
            return False, "El teléfono es obligatorio."

        if not username.strip():
            return False, "El nombre de usuario es obligatorio."

        return ProfileRepository.update_user_profile(
            user_id,
            nombre.strip(),
            apellido.strip(),
            telefono.strip(),
            username.strip()
        )