from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Notification
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Post)
def post_created_notification(sender, instance, created, **kwargs):
    if created:
        message = f"New post created by {instance.user.email}"
        Notification.objects.create(user=instance.user, message=message)
        send_notification_email(instance.user.email, message)

def send_notification_email(to_email, message):
    subject = 'New Post Created'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email])