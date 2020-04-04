import pytest


@pytest.mark.skipif('True==True')
@pytest.mark.usefixtures('client', 'token', 'header_key')
class TestRatio:

    def test_ratio_gender(self, client, token, header_key):
        payload = {
            'country': 'China',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }
        headers = {
            header_key: token,
        }
        response = client.get('/ratio/gender', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_ratio_age(self, client, token, header_key):
        payload = {
            'country': 'China',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }
        headers = {
            header_key: token,
        }
        response = client.get('/ratio/age', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_ratio_rehabilitation(self, client, token, header_key):
        payload = {
            'country': 'China',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }
        headers = {
            header_key: token,
        }
        response = client.get('/ratio/rehabilitatio', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200

    def test_ratio_sars(self, client, token, header_key):
        payload = {
            'country': 'China',
            'stime': '2020-03-24',
            'etime': '2020-03-22'
        }
        headers = {
            header_key: token,
        }
        response = client.get('/ratio/sars', params=payload, headers=headers)
        print("response: ", response)
        assert response.status_code == 200
