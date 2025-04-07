from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Reply, Notification
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        message = f"New comment on post {instance.post.id}"
        Notification.objects.create(user=instance.post.user, message=message)
        send_notification_email(instance.post.user.email, message)

@receiver(post_save, sender=Reply)
def reply_notification(sender, instance, created, **kwargs):
    if created:
        message = f"New reply to comment {instance.comment.id}"
        Notification.objects.create(user=instance.comment.post.user, message=message)
        send_notification_email(instance.comment.post.user.email, message)

def send_notification_email(to_email, message):
    subject = 'New Notification'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email])

