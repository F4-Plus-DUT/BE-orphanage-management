from api_user.models import Role
from api_user.statics import RoleData
from api_user.utils import split_scopes, get_default_scopes, concat_scopes


class RoleService:
    @classmethod
    def get_role_customer(cls) -> Role:
        """
        Get the customer role.
        Role model have to have a customer role. If not, pls contact your leader now!!!

        :return: The customer role.
        """
        role = Role.objects.by_id(RoleData.CUSTOMER.value.get('id'))
        if not role:
            raise Exception('Missing default role')
        return role

    @classmethod
    def get_role_employee(cls) -> Role:
        """
        Get the employee role.
        Role model have to have a customer role. If not, pls contact your leader now!!!

        :return: The employee role.
        """
        role = Role.objects.by_id(id=RoleData.EMPLOYEE.value.get('id'))
        if not role:
            raise Exception('Missing employee role')
        return role

    @classmethod
    def mock_default_scope(cls, role: Role):
        default_scopes = set(split_scopes(get_default_scopes()))
        scopes = set(split_scopes(role.scope_text))
        new_default_scopes = default_scopes.difference(scopes)

        scopes = scopes.union(new_default_scopes) if new_default_scopes else scopes

        role.scope_text = concat_scopes(list(scopes))
        role.save()
