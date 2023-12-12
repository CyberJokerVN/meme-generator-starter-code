from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from typing import List
import subprocess


class PDFIngestor(IngestorInterface):
    allowed_exensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = []
        p = subprocess.Popen(
            ['pdftotext', '-nopgbrk', path, '-'], stdout=subprocess.PIPE
        )
        data = p.communicate()[0].decode()
        data = data.split('\r\n')
        for line in data:
            if line != '':
                data = line.split(' - ')
                quotes.append(QuoteModel(data[0], data[1]))
        return quotes