from rest_framework import serializers
from .models import Comment, Reply


class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = ['id', 'comment', 'text', 'created_at', 'updated_at'] 


class CommentSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'created_at','updated_at']

