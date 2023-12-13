from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from typing import List
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

class TextIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the text file and extract quotes.

        :param path: str - Path to the text file.
        :return: List[QuoteModel] - List of QuoteModel objects.
        """
        if not path.endswith('.txt'):
            logging.error(f"File at {path} is not a text file.")
            raise ValueError("Ingestor can only process text files.")

        try:
            quotes = []
            with open(path, 'r', encoding='utf-8') as fid:
                for line in fid.readlines():
                    line = line.strip()  # Removes leading/trailing whitespace
                    if line:
                        parts = line.split(' - ')
                        if len(parts) < 2:
                            logging.warning(f"Skipping improperly formatted line: {line}")
                            continue
                        quote = QuoteModel(parts[0], parts[1])
                        quotes.append(quote)

            logging.info(f"{len(quotes)} quotes successfully extracted from {path}.")
            return quotes

        except FileNotFoundError:
            logging.error(f"File at {path} was not found.")
            raise FileNotFoundError(f"No file found at {path}")

        except UnicodeDecodeError:
            logging.error(f"Unicode decoding error occurred for file {path}. Please check the file encoding.")
            raise

        except Exception as e:
            logging.error(f"An error occurred while parsing the text file: {e}")
            raise e
