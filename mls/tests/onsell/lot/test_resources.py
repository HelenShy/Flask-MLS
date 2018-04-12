from flask import url_for

from lib.tests import ViewTestMixin, assert_status_with_message


class TestLots(ViewTestMixin):
    def test_add_lot(self, client):
        """ Index renders successfully. """
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
        response_add = self.client.post('/api/onsell/lots', data=new_lot, follow_redirects=True)
        assert_status_with_message(200, response_add, 'message', 'Lot #2 was saved successfully')
        response_get = client.get(url_for('onsell.lots_user_lot_by_id', _id=1))
        assert_status_with_message(200, response_get, 'type', 'flat')
        assert_status_with_message(200, response_get, 'square', 400)


    def test_get_lots(self):
        """ Edit page renders successfully. """
        self.login()
        response = self.client.get(url_for('onsell.lots_user_lot'))

        assert response.status_code == 200

    def test_edit_lot(self, client):
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
        edit_lot = {
            'type': 'house',
            'description': 'very bright',
            'square': 400,
            'qty_rooms': 4,
            'parking': True,
            'garageSpaces': 2,
            'year_built': 2010,
            'price': 500,
            'status': 'active'
        }
        response_put = self.client.put(url_for('onsell.lots_user_lot_by_id', _id=1), data=edit_lot, follow_redirects=True)
        assert_status_with_message(200, response_put, 'message', 'Lot #1  was edited successfully')

        response_get = client.get(url_for('onsell.lots_user_lot_by_id', _id=1))
        assert_status_with_message(200, response_get, 'type', 'house')
        assert_status_with_message(200, response_get, 'square', 400)

    def test_delete_lot(self):
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
        response = self.client.delete(url_for('onsell.lots_user_lot_by_id', _id=1))

        assert_status_with_message(200, response, 'message', 'Lot #1  was deleted')

    def test_delete_non_existing_lot(self):
        """ Edit page renders successfully. """
        self.login()
        response = self.client.delete(url_for('onsell.lots_user_lot_by_id', _id=10))

        assert response.status_code == 500
