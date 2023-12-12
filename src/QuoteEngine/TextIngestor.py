from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

class TextIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        try:
            with open(path, 'r', encoding='utf-8') as fid:
                for line in fid.readlines():
                    line = line.strip()  # Removes leading/trailing whitespace
                    if len(line) > 0:
                        parts = line.split(' - ')
                        if len(parts) == 2:
                            quotes.append(QuoteModel(parts[0].strip(), parts[1].strip()))
                        else:
                            print(f"Line in file {path} is not in the expected format: '{line}'")
            return quotes
        except UnicodeDecodeError:
            print(f"Cannot decode the file {path} with 'utf-8' encoding.")
            return []
        except FileNotFoundError:
            print(f"The file {path} was not found.")
            return []
        except Exception as e:
            print(f"Error processing file {path}: {e}")
            return []
