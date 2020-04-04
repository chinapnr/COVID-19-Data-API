import pytest


@pytest.mark.usefixtures('client', 'token', 'header_key')
class TestPopulation:

    def test_population(self, client, token, header_key):
        headers = {
            header_key: token,
        }
        response = client.get('/population', headers=headers)
        print("response: ", response)
        assert response.status_code == 200
