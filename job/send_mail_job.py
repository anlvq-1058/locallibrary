from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail


@background(schedule=60)
def notify_user(user_id):
    # lookup user by id and send them a message
    print('hello', user_id)
    user = User.objects.get(pk=user_id)
    send_mail(subject='hello background job',
              message='test mail',
              from_email='locallibrary@book.com',
              recipient_list=[user.email])
