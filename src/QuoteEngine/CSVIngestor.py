from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from typing import List
import pandas as pd
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

class CSVIngestor(IngestorInterface):
    """
    CSVIngestor is a class that ingests quotes from a CSV file.
    It extends the IngestorInterface.
    """
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the CSV file and extract quotes.

        :param path: str - Path to the CSV file.
        :return: List[QuoteModel] - List of QuoteModel objects.
        """
        if not path.endswith('.csv'):
            logging.error(f"File at {path} is not a CSV file.")
            raise ValueError("Ingestor can only process CSV files.")

        try:
            qdf = pd.read_csv(path, header=0)
            quotes = []

            for _, row in qdf.iterrows():
                quote = QuoteModel(row['body'], row['author'])
                quotes.append(quote)

            logging.info(f"{len(quotes)} quotes successfully extracted from {path}.")
            return quotes

        except FileNotFoundError:
            logging.error(f"File at {path} was not found.")
            raise FileNotFoundError(f"No file found at {path}")

        except Exception as e:
            logging.error(f"An error occurred while parsing the CSV file: {e}")
            raise e
