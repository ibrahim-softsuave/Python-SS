import random

from .models import User
from django.core.mail import EmailMessage

from storages.backends.s3boto3 import S3Boto3Storage

def otp_generator(user):

    numbers = '0123456789'

    user = User.objects.get(email=user.email)
    while True:
        otp = ''.join(random.choice(numbers) for x in range(6))
        if not User.objects.filter(otp=otp).exists():
            return otp



class Util:

    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
        
        
def upload_file(file):
    media_storage = S3Boto3Storage()
    file_path = 'test'
    
    path = media_storage.save(f'{file_path}/{file.name}', file)
    
    return path