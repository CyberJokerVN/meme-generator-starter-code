class QuoteModel:
    """
    A model representing a quote, including its text and author.

    Attributes:
        body (str): The text of the quote.
        author (str): The name of the author of the quote.
    """

    def __init__(self, body: str, author: str):
        """
        Initializes a new instance of QuoteModel.

        :param body: The text of the quote.
        :param author: The name of the author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """
        Provides a string representation of the QuoteModel instance.

        :return: A string in the format '"quote text" - author'.
        """
        return f'"{self.body}" - {self.author}'
