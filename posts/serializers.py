from rest_framework import serializers
from .models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):

    #tags = TagSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'text_content', 'image', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


    def create(self, validated_data):
        tags_data = validated_data.pop('tags',[])
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data: 
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            post.tags.add(tag)
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags',[])
        instance.text_content = validated_data.get('text_content', instance.text_content)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            instance.tags.add(tag)

        return instance