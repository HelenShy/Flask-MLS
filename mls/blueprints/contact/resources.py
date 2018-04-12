from flask import Blueprint, request
from flask_restplus import Api, Resource, reqparse

from lib.flask_mailplus import send_template_message

contact_blueprint = Blueprint('contact', __name__, url_prefix='/api/contact', template_folder='templates')
contact_api = Api(contact_blueprint)

ns = contact_api.namespace('mail', description='...')

parser = contact_api.parser()
parser.add_argument('email', type=str, help='This field cannot be blank', required=True, location='form')
parser.add_argument('message', type=str, help='This field cannot be blank', required=True, location='form')


@ns.route('')
class Contact(Resource):
    @ns.expect(parser)
    def post(self):
        data = parser.parse_args()
        from mls.blueprints.contact.tasks import deliver_contact_email
        deliver_contact_email.delay(data['email'],
                                    data['message'])
        return {'message': 'Mail was sent successfully'}

    # def post(self):
    #     from mls.blueprints.contact.tasks import deliver_contact_email
    #     deliver_contact_email.delay(request.get('email'),
    #                                 request.get('message'))
    #     return None

#
# def deliver_contact_email(email, message):
#     """
#     Send a contact email.
#
#     :param email: Visitor email
#     :param message: Visitor message
#     :return:
#     """
#     ctx = {'email': email, 'message': message}
#
#     send_template_message(subject='House Stage Contact',
#                           sender=email,
#                           recipients=['le0nana0888@gmail.com'],
#                           reply_to=email,
#                           template='contact/mail/index', ctx=ctx)
#
#     return {'message': 'Mail was sent successfully'}


