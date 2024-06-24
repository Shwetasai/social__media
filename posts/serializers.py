from rest_framework import serializers
from .models import Post
from Users.models import CustomUser
from .models import Post, Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)
    
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