
from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel

class IngestorInterface(ABC):
    allowed_exensions = []

    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        return path.split('.')[-1] in cls.allowed_exensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass
