from rest_framework import serializers
from .models import Comment, Reply


class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'created_at', 'replies']

