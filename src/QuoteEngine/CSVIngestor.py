from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from typing import List
import pandas as pd


class CSVIngestor(IngestorInterface):
    allowed_exensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        qdf = pd.read_csv(path, header=0)
        quotes = [None] * len(qdf)
        for i in range(len(qdf)):
            quotes[i] = QuoteModel(qdf.loc[i].body, qdf.loc[i].author)
        return quotes