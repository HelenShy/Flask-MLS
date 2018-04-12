from flask import url_for

from lib.tests import ViewTestMixin, assert_status_with_message


class TestGeo(ViewTestMixin):
    def test_geo(self):
        """ Edit page renders successfully. """
        self.login()
        geo = {
            'lat': 10,
            'lng': 50,
        }
        response_post = self.client.post(url_for('onsell.geo_lot_geo', _id=1), data=geo, follow_redirects=True)
        assert_status_with_message(200, response_post, 'message', 'Geo location for lot #1 was added')

        response_get = self.client.get(url_for('onsell.geo_lot_geo', _id=1), follow_redirects=True)
        assert_status_with_message(200, response_get, 'lat', 10)

        geo_changed = {
            'lat': 20,
            'lng': 50,
        }

        response_put = self.client.put(url_for('onsell.geo_lot_geo', _id=1), data=geo_changed, follow_redirects=True)
        assert_status_with_message(200, response_put, 'message', 'Geo location for lot #1 was changed')

        response_get = self.client.get(url_for('onsell.geo_lot_geo', _id=1), follow_redirects=True)
        assert_status_with_message(200, response_get, 'lat', 20)

        response_delete = self.client.delete(url_for('onsell.geo_lot_geo', _id=1), follow_redirects=True)
        assert_status_with_message(200, response_delete, 'message', 'Geo location for lot #1 was removed successfully')
