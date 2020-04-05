import json

import pytest


@pytest.mark.usefixtures('client', 'headers')
class TestInfection:

    def test_infection_country_tc01(self, client, headers):
        # db has data BETWEEN 2020-03-22 2020-03-24
        country = 'China'
        payload = {
            'country': country,
            'stime': '2020-03-22',
            'etime': '2020-03-24',
            'detail': 'false'
        }
        response = client.get('/infection/country', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data.get('name') == country
        assert not response_data.get('area')

    @pytest.mark.skipif('True==True')
    def test_infection_country_tc02(self, client, headers):
        # db has no data BETWEEN 2020-03-25 2020-03-26
        country = 'China'
        payload = {
            'country': country,
            'stime': '2020-03-25',
            'etime': '2020-03-26',
            'detail': 'false'
        }

        response = client.get('/infection/country', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert not response_data

    def test_infection_country_tc03(self, client, headers):
        # db has data BETWEEN 2020-03-22 2020-03-24
        # look up detail
        country = 'China'
        payload = {
            'country': country,
            'stime': '2020-03-22',
            'etime': '2020-03-24',
            'detail': 'true'
        }
        response = client.get('/infection/country', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data
        assert response_data.get('name') == country
        assert response_data.get('area')

    def test_infection_city(self, client, headers):
        country = 'China'
        area = 'Chongqing'
        payload = {
            'country': country,
            'area': area,
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }

        response = client.get('/infection/city', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_infection_global_detail(self, client, headers):
        payload = {
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }
        response = client.get('/infection/global', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data
