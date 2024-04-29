from uuid import UUID
from dataclasses import dataclass

from model.fertilizer import Fertilizer


@dataclass
class FertilizerList:
    uuid_list: list[UUID]
    fertilizer_list: list[Fertilizer]

    def __init__(self, uuid_list: list[UUID] = None):
        if uuid_list is None:
            self.uuid_list = []
        else:
            self.uuid_list = uuid_list
        self.fertilizer_list = self.fetch_fertilizer_list()

    def insert_fertilizer(self, fertilizer: Fertilizer):
        self.fertilizer_list.append(fertilizer)
        self.uuid_list.append(fertilizer.uuid)

    def fetch_fertilizer_list(self) -> list[Fertilizer]:
        return self.fertilizer_list
