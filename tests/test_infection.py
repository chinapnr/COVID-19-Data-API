import json

import pytest


@pytest.mark.usefixtures('client', 'headers')
class TestInfection:

    def test_infection_region_tc01(self, client, headers):
        # db has data BETWEEN 2020-03-22 2020-03-24
        region = 'China'
        payload = {
            'region': region,
            'start_date': '2020-03-22',
            'end_date': '2020-03-24',
            'include_hmt': 'false'
        }
        response = client.get('/infection/region', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_infection_region_tc02(self, client, headers):
        # db has no data BETWEEN 2020-03-25 2020-03-26
        region = 'China'
        payload = {
            'region': region,
            'start_date': '2020-03-25',
            'end_date': '2020-03-26',
            'include_hmt': 'false'
        }

        response = client.get('/infection/region', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_infection_region_tc03(self, client, headers):
        # db has data BETWEEN 2020-03-22 2020-03-24
        # look up detail
        region = 'China'
        payload = {
            'region': region,
            'start_date': '2020-03-22',
            'end_date': '2020-03-24',
            'include_hmt': 'true'
        }
        response = client.get('/infection/region', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_infection_region_detail(self, client, headers):
        region = 'China'
        payload = {
            'region': region,
            'start_date': '2020-03-22',
            'end_date': '2020-03-24',
            'include_hmt': 'true'
        }
        response = client.get('/infection/region/detail', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_infection_area(self, client, headers):
        region = 'China'
        area = 'Chongqing'
        payload = {
            'region': region,
            'area': area,
            'start_date': '2020-03-22',
            'end_date': '2020-03-24'
        }

        response = client.get('/infection/area', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_infection_global(self, client, headers):
        response = client.get('/infection/global', headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data
