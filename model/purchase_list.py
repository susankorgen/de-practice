from uuid import UUID
from dataclasses import dataclass

from model.purchase import Purchase


@dataclass
class PurchaseList:
    uuid_list: list[UUID]
    purchase_list: list[Purchase]

    def __init__(self, uuid_list: list[UUID] = None):
        if uuid_list is None:
            self.uuid_list = []
        else:
            self.uuid_list = uuid_list
        self.purchase_list = self.fetch_purchase_list()

    def insert_purchase(self, purchase: Purchase):
        self.purchase_list.append(purchase)
        self.uuid_list.append(purchase.uuid)

    def fetch_purchase_list(self) -> list[Purchase]:
        return self.purchase_list
