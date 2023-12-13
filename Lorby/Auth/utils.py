from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken


def send_confirmation_email(self, user):
    expiration_token = timezone.now() + timezone.timedelta(minutes=5)
    token = RefreshToken.for_user(user)
    token['exp'] = int(expiration_token.timestamp())
    protocol = self.request.scheme
    current_site = get_current_site(self.request).domain
    absurl = f'{protocol}://{current_site}/auth/confirm-email/{token}/'
    subject = f'Подтвердите Ваш e-mail'
    email_body = f'Пожалуйста, перейдите по ссылке, для подтверждения Вашей почты: {absurl} ' \
                 f'Ссылка работает всего 5 минут, если не успели попросите нас выслать вам еще одно письмо. ' \
                 f'Спасибо, что присоединились!'
    send_mail(subject, email_body, settings.EMAIL_FROM, [user.email])

