from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from bson import ObjectId

class Status:
    TODO = "TODO"
    PROCESSING = "PROCESSING"
    DONE = "DONE"

    TIMEOUT = "TIMEOUT" # 一直 PROCESSING 的任务，超时
    FAIL = "FAIL"
    FEZZ = "FEZZ"
    """ 特殊: 任务冻结 """

@dataclass
class Task:
    _id: ObjectId
    id: int
    status: Status
    archivist: str

    claimed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


    def __post_init__(self):
        assert self.status in Status.__dict__.values()

    def __repr__(self):
        return f"Task({self.id}, status={self.status})"

    def __init__(self, _id, id, status, archivist, claimed_at, updated_at):
        self._id = _id
        self.id = id
        self.status = status
        self.archivist = archivist
        self.claimed_at = claimed_at
        self.updated_at = updated_at