from flask import url_for


class TestApi(object):
    def test_hello_page(self, client):
        #response = client.get(url_for('auth.HiWorld.get'))
        response = client.get('/api/ns_hello/hello')
        assert response.status_code == 200
