from flask import url_for

from lib.tests import ViewTestMixin, assert_status_with_message
from io import BytesIO


class TestPhoto(ViewTestMixin):
    def test_photos(self):
        """ Edit page renders successfully. """
        self.login()
        response_get = self.client.get(url_for('onsell.photos_lot_photos', _id=2), follow_redirects=True)
        assert_status_with_message(200, response_get, 'message', 'Lot #2 does not have loaded photos yet.')

    def test_photo(self):
        """ Edit page renders successfully. """
        self.login()
        response_get = self.client.get(url_for('onsell.photos_lot_photo', _id=2, photo_id=1), follow_redirects=True)
        assert_status_with_message(200, response_get, 'message', 'Photo does not exist')

    def test_load_photo(self):
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
        photo = {
            'file': (BytesIO(b'my file contents'), 'test.jpeg')
        }
        response_post = self.client.post(url_for('onsell.photos_lot_photos', _id=3), data=photo, follow_redirects=True)
        assert_status_with_message(200, response_post, 'message', 'Photo was saved succesfully')

        response_get = self.client.get(url_for('onsell.photos_lot_photo', _id=3, photo_id=1), follow_redirects=True)
        assert_status_with_message(200, response_get, 'photo_path', '3-test.jpeg')

        response_delete = self.client.delete(url_for('onsell.photos_lot_photo', _id=3, photo_id=1), follow_redirects=True)
        assert_status_with_message(200, response_delete, 'message', 'Photo was removed successfully')

    def test_load_photos(self):
        """ Edit page renders successfully. """
        self.login()
        photo = {
            'file': (BytesIO(b'my file contents'), 'test.jpeg')
        }
        response_post = self.client.post(url_for('onsell.photos_lot_photos', _id=3), data=photo,
                                         follow_redirects=True)
        assert_status_with_message(200, response_post, 'message', 'Photo was saved succesfully')

        response_get = self.client.get(url_for('onsell.photos_lot_photos', _id=3), follow_redirects=True)
        assert response_get.status_code == 200

        response_delete = self.client.delete(url_for('onsell.photos_lot_photos', _id=3),
                                             follow_redirects=True)
        assert_status_with_message(200, response_delete, 'message', 'Photos for lot #3 were removed successfully')
