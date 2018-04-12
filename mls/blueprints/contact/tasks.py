from lib.flask_mailplus import send_template_message
from mls.app import create_celery_app

celery = create_celery_app()


@celery.task()
def deliver_contact_email(email, message):
    """
    Send a contact email.

    :param email: Visitor email
    :param message: Visitor message
    :return:
    """
    ctx = {'email': email, 'message': message}

    send_template_message(subject='House Stage Contact',
                          sender=email,
                          recipients=[celery.conf.get('MAIL_USERNAME')],
                          reply_to=email,
                          template='contact/mail/index', ctx=ctx)

    return None
