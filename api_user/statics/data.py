from enum import Enum


class RoleData(Enum):
    ADMIN = {
        "id": "7a8f585dccb049ada11653bd0f550d59",
        "name": "Super Administrator",
        "scope_text": "__all__",
        "description": "administrator",
    }

    CUSTOMER = {
        "id": "45905ee5131544cf8f8235cb9d838b75",
        "name": "Customer",
        "scope_text": "",
        "description": "Customer of F4plus orphanage",
    }

    EMPLOYEE = {
        "id": "af91d25cadc346fd8c4010bbba8c1fe7",
        "name": "Employee",
        "scope_text": "",
        "description": "Employee of F4plus orphanage",
    }
