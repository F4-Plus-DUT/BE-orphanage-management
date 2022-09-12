from rest_framework_simplejwt.exceptions import TokenError
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
            'access_token': str(token.access_token),
            'refresh_token': str(token),
        }
        return data

    @classmethod
    def refresh_new_token(cls, token: str):
        """
        Generate totally new token (refresh token and access token)
        :param token: refresh token
        :return: dictionary with refresh_token and access_token
        """
        data = {}
        try:
            token_instance = RefreshToken(token=token)
            payload = token_instance.payload
            account_id = payload.get('user_id', '')
            account = Account.objects.by_id(account_id)
            if account:
                new_token = RefreshToken.for_user(account)
                data = {
                    'refresh_token': str(new_token),
                    'access_token': str(new_token.access_token)
                }
        except TokenError:
            pass
        return data
