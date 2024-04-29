from uuid import UUID, uuid4
from dataclasses import dataclass


@dataclass
class Fertilizer:
    uuid: UUID
    consumer_uuid: UUID
    purchase_uuid: UUID

    def __init__(self, consumer_uuid, purchase_uuid):
        if consumer_uuid is None or purchase_uuid is None:
            raise ValueError("Consumer UUID and Purchase UUID cannot be None")
        self.uuid = uuid4()
        self.consumer_uuid = consumer_uuid
        self.purchase_uuid = purchase_uuid
