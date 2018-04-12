from lib.tests import ViewTestMixin, assert_status_with_message


class TestContact(ViewTestMixin):
    def test_contact_page(self):
        """ Contact page should respond with a success 200. """
        self.login()
        mail = {
            'email': 'test@mail.com',
            'message': 'Test'
        }
        response = self.client.post('/api/contact/mail', data=mail, follow_redirects=True)
        assert_status_with_message(200, response, 'message', 'Mail was sent successfully')
