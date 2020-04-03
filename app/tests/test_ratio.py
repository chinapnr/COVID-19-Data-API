import pytest

from unittest import TestCase


@pytest.mark.usefixtures('client', 'token')
class RatioTest(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_ratio_gender(self, client, token) -> None:
        self.fail()

    def test_ratio_age(self, client, token) -> None:
        self.fail()

    def test_ratio_rehabilitation(self, client, token) -> None:
        self.fail()

    def test_ratio_sars(self, client, token) -> None:
        self.fail()
