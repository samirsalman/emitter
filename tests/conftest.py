import logging

import pytest


@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(level=logging.DEBUG)
