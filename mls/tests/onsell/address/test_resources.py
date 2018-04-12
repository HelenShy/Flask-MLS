from flask import url_for

from lib.tests import ViewTestMixin, assert_status_with_message


class TestAddress(ViewTestMixin):
    def test_address(self):
        """ Edit page renders successfully. """
        self.login()
        new_lot = {
            'type': 'flat',
            'description': 'very bright',
            'square': 400,
            'qty_rooms': 4,
            'parking': True,
            'garageSpaces': 2,
            'year_built': 2010,
            'price': 500,
            'status': 'active'
        }
        self.client.post('/api/onsell/lots', data=new_lot, follow_redirects=True)
        address = {
            'city': 'Kiev',
            'street': 'Gorkogo',
            'house_number': 7
        }
        response_post = self.client.post(url_for('onsell.address_lot_address', _id=1), data=address, follow_redirects=True)
        assert_status_with_message(200, response_post, 'message', 'Address for lot #1 was added')

        response_get = self.client.get(url_for('onsell.address_lot_address', _id=1), follow_redirects=True)
        assert_status_with_message(200, response_get, 'city', 'Kiev')

        geo_changed = {
            'city': 'Kiev',
            'street': 'Gorkogo',
            'house_number': 8
        }

        response_put = self.client.put(url_for('onsell.address_lot_address', _id=1), data=geo_changed, follow_redirects=True)
        assert_status_with_message(200, response_put, 'message', 'Address for lot #1 was changed')

        response_get = self.client.get(url_for('onsell.address_lot_address', _id=1), follow_redirects=True)
        assert_status_with_message(200, response_get, 'house_number', 8)

        response_delete = self.client.delete(url_for('onsell.address_lot_address', _id=1), follow_redirects=True)
        assert_status_with_message(200, response_delete, 'message', 'Address for lot #1 was removed successfully')
