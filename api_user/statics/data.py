from enum import Enum


class AccountData:
    accounts = [
        {
            "id": '9476092d3e0b4490a8fdeb6ec3b188f3',
            "email": "dinhgiabao2807@gmail.com",
        },
        {
            "id": '6070a85db2ee47019c9e8cd5d8306eaf',
            "email": "trancongviet0710@gmail.com",
        },
        {
            "id": '68d266c95ce84c2cb808473f51dc4ba2',
            "email": "hohoangthien1204@gmail.com",
        },
    ]


class ProfileData:
    profiles = [
        {
            "name": "Dinh Gia Bao",
            "gender": 2,
            "occupation": "Student"
        },
        {
            "name": "Tran Cong Viet",
            "gender": 1,
            "occupation": "Student"
        },
        {
            "name": "Ho Hoang Thien",
            "gender": 1,
            "occupation": "Student"
        }
    ]


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

    ADOPT_MANAGER = {
        "id": "cd3f70ce328a408b83ba205a331735eb",
        "name": "Adopt Manager",
        "scope_text": "adopt_request:view_adopt_request adopt_request:edit_adopt_request",
        "description": "Management Adopt Request of F4plus orphanage",
    }
