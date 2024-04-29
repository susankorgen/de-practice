from uuid import UUID
from dataclasses import dataclass


@dataclass
class UUIDList:
    values: list[UUID]

    def __init__(self):
        self.values = []

    def add_item(self, uuid: UUID):
        self.values.append(uuid)

    def remove_item(self, uuid: UUID):
        self.values.remove(uuid)
