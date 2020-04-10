import json

import pytest


@pytest.mark.usefixtures('client', 'headers')
class TestOther:

    def test_other_population(self, client, headers):
        region = 'US'
        payload = {
            'region': region,
        }
        response = client.get('/other/populations', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_other_region_list(self, client, headers):
        response = client.get('/other/region_list', headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data

    def test_other_area_list(self, client, headers):
        region = 'US'
        payload = {
            'region': region,
            'include_hmt': 'true',
        }
        response = client.get('/other/area_list', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data
