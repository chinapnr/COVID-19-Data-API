import pytest


@pytest.mark.usefixtures('client')
class TestHealth:

    def test_health(self, client):
        response = client.head('/health')
        assert response.status_code == 200
