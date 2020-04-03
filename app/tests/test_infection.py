import pytest

from unittest import TestCase


@pytest.mark.usefixtures('client', 'token')
class InfectionTest(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_infection_daily(self, client, token) -> None:
        self.fail()

    def test_infection_area(self, client, token):
        self.fail()

    def test_infection_country(self, client, token):
        self.fail()

    def test_infection_country_detail(self, client, token):
        self.fail()

    def test_infection_city(self, client, token):
        self.fail()

    def test_infection_city_detail(self, client, token):
        self.fail()
