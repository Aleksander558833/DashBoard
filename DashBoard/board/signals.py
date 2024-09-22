from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, Responses


@receiver(post_save, sender=Post)
def post_create(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.all().values_list('email', flat=True)
    subject = f'Добавлено новое объявление {instance.title}'
    text_content = (
        f'Объявление {instance.title} добавлено в категорию {instance.category}\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.send()

@receiver(post_save, sender=Responses)
def send_response(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.status:
        mail = instance.author.email
        send_mail(
            subject='',
            message=f'Ваш отклик на {instance.post} принят',
            recipient_list=[mail],
            from_email=None,
            fail_silently=False,
        )
    else:
        mail = instance.post.author.email
        send_mail(
            subject='',
            message=f'На вашу публикацию {instance.post} пришел отклик от {instance.author}',
            recipient_list=[mail],
            from_email=None,
            fail_silently=False,
        )