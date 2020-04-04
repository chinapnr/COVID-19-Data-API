import pytest


@pytest.mark.usefixtures('client', 'token', 'header_key')
class TestInfection:

    def test_infection_daily(self, client, token, header_key):
        payload = {
            'country': 'China'
        }
        headers = {
            header_key: token,
        }
        response = client.get('/infection/detail', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_infection_area(self, client, token, header_key):
        payload = {
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }

        headers = {
            header_key: token,
        }
        response = client.get('/infection/area', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_infection_country(self, client, token, header_key):
        payload = {
            'country': 'China',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }

        headers = {
            header_key: token,
        }
        response = client.get('/infection/country', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_infection_country_detail(self, client, token, header_key):
        payload = {
            'country': 'China',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }
        headers = {
            header_key: token,
        }
        response = client.get('/infection/country/detail', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_infection_city(self, client, token, header_key):
        payload = {
            'city': 'Chongqing',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }

        headers = {
            header_key: token,
        }
        response = client.get('/infection/city', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_infection_city_detail(self, client, token, header_key):
        payload = {
            'city': 'Chongqing',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }

        headers = {
            header_key: token,
        }
        response = client.get('/infection/city/detail', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_infection_global_detail(self, client, token, header_key):

        headers = {
            header_key: token,
        }
        response = client.get('/infection/global/detail', headers=headers)
        print("response: ", response)
        assert response.status_code == 200
