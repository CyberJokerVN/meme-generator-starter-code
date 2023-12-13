from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from typing import List
import subprocess
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

class PDFIngestor(IngestorInterface):
    """
    PDFIngestor is a class that ingests quotes from a PDF file.
    It extends the IngestorInterface and uses an external tool to convert PDF to text.
    """
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the PDF file and extract quotes.

        :param path: str - Path to the PDF file.
        :return: List[QuoteModel] - List of QuoteModel objects.
        """
        if not path.endswith('.pdf'):
            logging.error(f"File at {path} is not a PDF file.")
            raise ValueError("Ingestor can only process PDF files.")

        try:
            # Using subprocess to call pdftotext tool
            p = subprocess.Popen(
                ['pdftotext', '-nopgbrk', path, '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = p.communicate()

            if stderr:
                logging.error(f"Error in processing PDF file {path}: {stderr.decode()}")
                raise Exception(stderr.decode())

            data = stdout.decode().split('\r\n')
            quotes = []

            for line in data:
                if line != '':
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

        except Exception as e:
            logging.error(f"An error occurred while parsing the PDF file: {e}")
            raise e
