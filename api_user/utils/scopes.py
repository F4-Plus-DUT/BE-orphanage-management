from typing import List
from core.settings import SCOPES, DEFAULT_SCOPES


def get_all_scopes() -> str:
    return " ".join(SCOPES.keys())


def get_default_scopes() -> str:
    return " ".join(DEFAULT_SCOPES.keys())


def split_scopes(scopes_text: str) -> List[str]:
    return scopes_text.split(' ')


def concat_scopes(scopes: List[str]) -> str:
    return " ".join(scope for scope in scopes)


def is_valid_auth(scope: str, user) -> bool:
    roles = user.roles.all()
    scopes = ""
    for role in roles:
        scopes += (role.scope_text + " ")
    if scopes.__contains__("__all__"):
        scopes = " ".join(SCOPES.keys())
    list_scopes = set(split_scopes(scopes))
    return True if scope in list_scopes else False
