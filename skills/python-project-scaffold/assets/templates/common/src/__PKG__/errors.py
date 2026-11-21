"""Exception types raised on purpose by this package.

Each error carries a plain-language message that is safe to show to a user.
Messages never contain secrets.
"""


class __ERROR_BASE__(Exception):
    """Base class for every error this package raises on purpose."""


class ConfigError(__ERROR_BASE__):
    """The configuration is missing or invalid."""
