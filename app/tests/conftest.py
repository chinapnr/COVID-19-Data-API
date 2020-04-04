import os

import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def token():
    # test api key
    return 'a35b6acef477d2beed9f075dc1efd5b2'


@pytest.fixture
def header_key():
    return os.getenv("HEADER_KEY")
