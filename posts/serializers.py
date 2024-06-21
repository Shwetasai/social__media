from rest_framework import serializers
from .models import Post
from Users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']

class PostSerializer(serializers.ModelSerializer):
    tags = UserSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'text_content', 'image', 'tags', 'tag_ids', 'created_at', 'updated_at']
        read_only_fields = ['user', 'tags', 'created_at', 'updated_at']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tag_ids)
        return post

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        
        
        if not tag_ids and not instance.tags.exists():
            raise serializers.ValidationError("At least one tag must be present.")
        
        instance.text_content = validated_data.get('text_content', instance.text_content)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        
        current_tags = set(instance.tags.all())
        new_tags = set(tag_ids)
        
        tags_to_add = new_tags - current_tags
        tags_to_remove = current_tags - new_tags
        
        for tag in tags_to_remove:
            instance.tags.remove(tag)
        
        for tag in tags_to_add:
            instance.tags.add(tag)
        
        return instance
