from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel

class IngestorInterface(ABC):
    """
    IngestorInterface is an abstract base class that defines the structure for various ingestor classes.

    Each ingestor class that extends this interface can parse a specific file type and must implement
    the parse method. The can_ingest class method checks if a given file can be ingested by the ingestor.
    """
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Check if the given file can be ingested based on its extension.

        :param path: str - Path to the file.
        :return: bool - True if the file can be ingested, False otherwise.
        """
        return path.split('.')[-1] in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Abstract method to parse a file and extract quotes.

        This method must be implemented by all subclasses of IngestorInterface.

        :param path: str - Path to the file.
        :return: List[QuoteModel] - List of extracted QuoteModel objects.
        """
        pass
