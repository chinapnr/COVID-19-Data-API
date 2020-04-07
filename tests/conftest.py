import os

import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def headers():
    header_key = os.getenv("HEADER_KEY")
    token = 'a35b6acef477d2beed9f075dc1efd5b2'
    return {header_key: token}
