import pytest


@pytest.mark.usefixtures('client')
class TestAuthentication:

    def test_authentication_register(self, client):
        payload = {
            "email": "rex_yan@126.com"
        }

        response = client.post('/authentication/register', json=payload)
        assert response.status_code == 400
