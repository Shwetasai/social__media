from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Followers, Notification

@receiver(post_save, sender=Followers)
def follow_notification(sender, instance, created, **kwargs):
    if created:
        message = f"{instance.follower.username} is now following you."
        Notification.objects.create(user=instance.following, message=message)
        send_notification_email(instance.following.email, message)

def send_notification_email(to_email, message):
    subject = 'New Follower'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email])
