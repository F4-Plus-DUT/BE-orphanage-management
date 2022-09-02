from rest_framework_simplejwt.tokens import RefreshToken

from api_user.models import Account


class TokenService:
    @classmethod
    def generate_by_account(cls, account: Account) -> dict:
        """

        :param account:
        :return: data with access_token and refresh_token
        """
        token = RefreshToken.for_user(account)
        data = {
            "access_token": str(token.access_token),
            "refresh_token": str(token),
        }
        return data
