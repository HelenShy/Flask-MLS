from flask import url_for
from lib.tests import ViewTestMixin, assert_status_with_message


class TestApi(ViewTestMixin):
    def test_register_page(self):
        user = {'username': 'test',
                'password': 'test123',
                'email': 'test@mail.com'}
        response = self.client.post('/api/auth/users/register', data=user)
        assert_status_with_message(200, response, 'register', 'True')

    def test_login_page(self):
        response = self.login()
        assert_status_with_message(200, response, 'login', 'True')

    def test_edit_user_page(self):
        self.login()
        user = {'username': 'admin',
                'email': 'new@mail.com',
                'password': 'devpassword'}
        response = self.client.put('/api/auth/users/edit', data=user)
        assert_status_with_message(200, response, 'message', 'User was edited successfully')

    def test_logout_page(self):
        self.login()
        response = self.client.delete(url_for('auth.users_user_logout_access'), follow_redirects=True)
        assert_status_with_message(200, response, 'logout', 'True')

    def test_get_user(self):
        self.login()
        response = self.client.get(url_for('auth.users_user_details', id=1), follow_redirects=True)
        assert_status_with_message(200, response, 'username', 'admin')

    def test_refresh_token(self):
        self.login()
        response = self.client.post(url_for('auth.token_token_refresh'), follow_redirects=True)
        assert_status_with_message(200, response, 'refresh', 'True')

    def test_get_users(self):
        self.login()
        response = self.client.get(url_for('auth.users_all_users'), follow_redirects=True)
        assert response.status_code == 200

