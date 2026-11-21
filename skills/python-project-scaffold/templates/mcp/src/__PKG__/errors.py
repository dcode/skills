"""Exception types raised on purpose by this package.

Each error carries a plain-language message that is safe to show to the agent
and the user. Messages never contain secrets.
"""


class __ERROR_BASE__(Exception):
    """Base class for every error this package raises on purpose."""


class ConfigError(__ERROR_BASE__):
    """The configuration is missing or invalid."""


class ConnectivityError(__ERROR_BASE__):
    """The service could not be reached (network, DNS, TLS trust, timeout)."""


class ApiError(__ERROR_BASE__):
    """The service answered with an unexpected status.

    Attributes:
        status: HTTP status code of the response.
    """

    def __init__(self, status: int, message: str) -> None:
        """Create the error.

        Args:
            status: HTTP status code of the response.
            message: Plain-language description of what went wrong.
        """
        super().__init__(message)
        self.status = status
