from uuid import UUID, uuid4
from dataclasses import dataclass


@dataclass
class Purchase:
    uuid: UUID
    consumer_uuid: UUID

    def __init__(self, consumer_uuid):
        if consumer_uuid is None:
            raise ValueError("Purchase Consumer UUID cannot be None")
        self.uuid = uuid4()
        self.consumer_uuid = consumer_uuid
