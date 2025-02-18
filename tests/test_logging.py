import logging

import pytest

from src.utils.logging import add_log_file, set_level


def test_set_level():
    set_level(logging.DEBUG)
    assert logging.getLogger().level == logging.DEBUG


def test_add_log_file(tmpdir):
    log_dir = tmpdir.mkdir("logs")
    add_log_file(logging.DEBUG, dirpath=str(log_dir), file_prefix="test")
    assert len(log_dir.listdir()) == 1
