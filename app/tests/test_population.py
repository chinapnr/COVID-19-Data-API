import pytest

from unittest import TestCase


@pytest.mark.usefixtures('client', 'token')
class PopulationTest(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_population(self, client, token) -> None:
        self.fail()
