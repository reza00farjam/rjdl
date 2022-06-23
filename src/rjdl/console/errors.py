from click import ClickException


class CLIConnectionError(ClickException):
    """
    Raised when connection to the server failed.
    """

    def __init__(self, message="Please check your connection"):
        super().__init__(message)


