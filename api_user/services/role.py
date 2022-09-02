from api_user.models import Role


class RoleService:
    @classmethod
    def get_default_role(cls) -> Role:
        """
        Get the default role.
        Role model have to have a default role. If not, pls contact your leader now!!!

        :return: The default role.
        """
        role = Role.objects.default()
        if not role:
            raise Exception('Missing default role')
        return role
