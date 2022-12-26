from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_link(email,token):
      subject='your password reset link'
      message=f'hi, follow this link to reset your password http://127.0.0.1:8000/accounts/password/reset/{token}'
      email_from=settings.EMAIL_HOST_USER
      recipient_list=[email]
      send_mail(subject,message,email_from,recipient_list)
      return True