import uuid
from dataclasses import dataclass

from model.purchase import Purchase


@dataclass
class Procedures:
    uuid: uuid
    purchase: list[Purchase] = None

    def __init__(self, purchase: list[Purchase] = None):
        self.uuid = uuid.uuid4()
        if purchase is None:
            self.purchase = []
        else:
            self.purchase = purchase
