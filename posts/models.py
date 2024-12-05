from django.db import models
from Users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    text_content = models.TextField(max_length=250)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = models.ManyToManyField(CustomUser, related_name='tagged_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.text_content[:20]}'



'''class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name'''