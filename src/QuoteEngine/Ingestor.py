from .IngestorInterface import IngestorInterface
from .CSVIngestor import CSVIngestor
from .TextIngestor import TextIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .QuoteModel import QuoteModel
from typing import List
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

class Ingestor(IngestorInterface):
    """
    Ingestor is a class that selects the appropriate ingestor for a given file format.
    It extends the IngestorInterface and uses other specific ingestors.
    """
    ingestors = [CSVIngestor, TextIngestor, DocxIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Selects the appropriate ingestor based on the file type and parses the file.

        :param path: str - Path to the file.
        :return: List[QuoteModel] - List of QuoteModel objects.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                try:
                    return ingestor.parse(path)
                except Exception as e:
                    logging.error(f"Error parsing file {path} with {ingestor.__name__}: {e}")
                    raise e

        logging.error(f"No suitable ingestor found for file {path}.")
        raise ValueError('Unsupported file format.')
