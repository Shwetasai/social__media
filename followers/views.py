from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from .serializers import FollowerSerializer 
from .models import Followers,CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class CustomFollowUserView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self,request):
        request_type =  request.data.get("request_type")
        follower_id = request.data.get("follower_id")
        following_id = request.data.get("following_id")
        try:
            follower = CustomUser.objects.get(id=follower_id)
            following = CustomUser.objects.get(id=following_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if request_type == 'follow':
            if Followers.objects.filter(follower=follower, following=following).exists():
                return Response({'error': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)
            Followers.objects.create(follower=follower, following=following)
            return Response({'message': 'Followed successfully'}, status=status.HTTP_201_CREATED)

        elif request_type == 'unfollow':
            follow_instance = Followers.objects.filter(follower=follower, following=following).first()
            if follow_instance:
                follow_instance.delete()
                return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Not following'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Please provide valid data"}, status=status.HTTP_400_BAD_REQUEST)
      
class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = FollowersListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = FollowingListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


