from .models import User
from celery import shared_task

from Test.utils import Util


@shared_task
def send_email_for_otp_verification(user_data):
    user = User.objects.get(email=user_data['email'])
    email_body = 'Hi ' + user.username + ' Please use below otp to verify your email\n' + user.otp
    data = {'email_body': email_body, 'email_subject': 'Verify your email', 'to_email': user_data['email']}
    Util.send_email(data=data)
    return "Successfully send email"