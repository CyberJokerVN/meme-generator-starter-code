from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from typing import List
import docx
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

class DocxIngestor(IngestorInterface):
    """
    DocxIngestor is a class that ingests quotes from a DOCX file.
    It extends the IngestorInterface.
    """
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the DOCX file and extract quotes.

        :param path: str - Path to the DOCX file.
        :return: List[QuoteModel] - List of QuoteModel objects.
        """
        if not path.endswith('.docx'):
            logging.error(f"File at {path} is not a DOCX file.")
            raise ValueError("Ingestor can only process DOCX files.")

        try:
            doc = docx.Document(path)
            quotes = []

            for line in doc.paragraphs:
                if line.text != '':
                    data = line.text.split(' - ')
                    if len(data) < 2:
                        logging.warning(f"Skipping improperly formatted line: {line.text}")
                        continue
                    quote = QuoteModel(data[0], data[1])
                    quotes.append(quote)

            logging.info(f"{len(quotes)} quotes successfully extracted from {path}.")
            return quotes

        except FileNotFoundError:
            logging.error(f"File at {path} was not found.")
            raise FileNotFoundError(f"No file found at {path}")

        except Exception as e:
            logging.error(f"An error occurred while parsing the DOCX file: {e}")
            raise e
