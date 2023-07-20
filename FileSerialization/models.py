from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Entity:
    pass


@dataclass
class Person:
    id: str
    firstName: str
    entities: List[Entity]

    def to_dict(self) -> dict:
        data = asdict(self)
        return data