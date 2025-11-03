from dataclasses import dataclass
from abc import ABC
from pathlib import Path


class Namespace(ABC):
    def get_fields(self) -> dict[str, object]:
        return self.__dict__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.get_fields()}"
