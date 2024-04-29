from dataclasses import dataclass


@dataclass
class Consumer:
    id: int

    def __init__(self, id: int):
        self.id = id
