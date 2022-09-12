from core.settings import SCOPES, DEFAULT_SCOPES


def get_all_scopes():
    return " ".join(SCOPES.keys())


def get_default_scopes():
    return " ".join(DEFAULT_SCOPES.keys())
