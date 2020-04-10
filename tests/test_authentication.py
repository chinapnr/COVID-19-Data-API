import json

import pytest


@pytest.mark.usefixtures('client')
class TestAuthentication:

    def test_authentication_register(self, client):
        payload = {
            "email": "string"
        }

        response = client.get('/infection/region', data=json.loads(payload))
        assert response.status_code == 200
