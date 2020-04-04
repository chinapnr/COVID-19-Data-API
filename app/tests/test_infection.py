import pytest

from unittest import TestCase
import os

import json


@pytest.mark.usefixtures('client', 'token', 'header_key')
class InfectionTest(TestCase):

    def test_infection_daily(self, client, token, header_key) -> None:
        payload = {
            '', ''
        }
        headers = {
            'Content-Type': 'application/json',
            header_key: token,
        }
        response = client.post('/daily', data=json.dumps(payload), headers=headers)
        print("response: ", response.data)
        assert response.status_code == 200
        self.coupon_code = response.json.get('data').get('coupon_code')

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

    def test_infection_global_detail(self, client, token):
        self.fail()
