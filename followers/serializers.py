from rest_framework import serializers
from .models import Followers
from Users.models import CustomUser
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class FollowerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Followers
        fields = ['follower', 'following']

    def create(self, validated_data):
        request = self.context.get('request')#getting requested data
        if not request:
            raise serializers.ValidationError('request context is required.')#context is missing
        follower=request.user#user who is requesting
        following_username=validated_data.get('following')#getting username for whom requesting from database

        try:
            following = CustomUser.objects.get(username=following_username)#getting follower username from database
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Follower user does not exist')#show error if customuser not found
        new_follower, created = Followers.objects.get_or_create(
                follower=follower,
                following=following
        )
        return new_follower
        
class FollowersListSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['followers']

    def get_followers(self, obj):
        followers = obj.followers.all()
        return FollowerSerializer(followers, many=True).data

class FollowingListSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['following']

    def get_following(self, obj):
        following = obj.following.all()
        return FollowerSerializer(following, many=True).data