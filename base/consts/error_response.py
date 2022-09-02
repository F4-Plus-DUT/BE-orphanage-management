from enum import Enum
from typing import List

from rest_framework import status
from rest_framework.response import Response


class ErrorResponseType(Enum):
    GENERAL = (4001, "{0}")
    CANT_DEACTIVATE = (4002, "{0} can't be deactivated")
    CANT_ACTIVATE = (4003, "{0} can't be activated")
    CANT_CREATE = (4004, "{0} can't be created")
    EMPTY = (4005, "{0} can't be empty")
    INVALID = (4005, "{0} is invalid")

    def __init__(self, code: int, error_message: str):
        self.code = code
        self.error_message = error_message


class ErrorResponse(Response):
    def __init__(self, error_response_type: ErrorResponseType, params: List, status_code: int = status.HTTP_400_BAD_REQUEST):
        message = error_response_type.error_message.format(*params)
        response_body = {
            "code": error_response_type.code,
            "message": message
        }
        super().__init__(response_body, status=status_code)
