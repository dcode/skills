import re

import pytest

import __PKG__
from __PKG__.errors import ConfigError, __ERROR_BASE__


def test_version_is_semver() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", __PKG__.__version__)


def test_errors_share_one_base() -> None:
    with pytest.raises(__ERROR_BASE__, match="bad setting"):
        raise ConfigError("bad setting")
