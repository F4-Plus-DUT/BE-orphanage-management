from enum import Enum


class AdoptRequestStatus:
    PENDING = "Pending"
    APPROVE = "Approve"
    REJECT = "Reject"
    CANCEL = "Cancel"
    CANCELING = "Canceling"
    CANCELED = "Canceled"


class MapAdoptRequestStatus(Enum):
    PENDING = {
        "id": 1,
        "value": "Pending"
    }
    APPROVE = {
        "id": 2,
        "value": "Approve"
    }
    REJECT = {
        "id": 3,
        "value": "Reject"
    }
    CANCEL = {
        "id": 4,
        "value": "Cancel"
    }
