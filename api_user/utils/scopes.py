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

