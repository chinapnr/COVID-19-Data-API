import json

import pytest


@pytest.mark.usefixtures('client', 'headers')
class TestPopulation:

    def test_population(self, client, headers):
        country = 'US'
        payload = {
            'country': country,
            'date': '2019'
        }
        response = client.get('/population', params=payload, headers=headers)
        assert response.status_code == 200
        print("response: ", response.text)
        response_data = json.loads(response.text)['data']
        assert response_data
