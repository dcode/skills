"""Structured logging to stderr.

The MCP server speaks its protocol on stdout, so a stray line there would
corrupt the conversation with the agent. Everything is logged to stderr:
readable on a terminal, one JSON object per line otherwise.
"""

import logging
import sys
from typing import Literal

import structlog

type LogLevel = Literal["debug", "info", "warning", "error"]

# Libraries that log every request at INFO, sometimes with full URLs.
_NOISY_LIBRARIES: tuple[str, ...] = ("httpx", "httpcore", "mcp")


def configure_logging(level: LogLevel = "info") -> None:
    """Send structured logs at or above a level to stderr.

    Args:
        level: The lowest level to emit.
    """
    number = logging.getLevelNamesMapping()[level.upper()]
    renderer: structlog.typing.Processor = (
        structlog.dev.ConsoleRenderer()
        if sys.stderr.isatty()
        else structlog.processors.JSONRenderer()
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(number),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=False,
    )
    logging.basicConfig(stream=sys.stderr, level=number, format="%(name)s: %(message)s", force=True)
    for name in _NOISY_LIBRARIES:
        logging.getLogger(name).setLevel(max(number, logging.WARNING))
