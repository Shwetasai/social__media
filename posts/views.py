from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import PostSerializer,TagSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Post, Tag 


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class PostmanageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        post = get_object_or_404(Post, id=id, user=request.user)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, id):
        post = get_object_or_404(Post, id=id, user=request.user)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id, user=request.user)
        post.tags.clear()   
        post.delete()
        return Response({'message': "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    '''def get_object(self, id, user):
        return get_object_or_404(Post, id=id, user=user)

    def get(self, request, id):
        post = self.get_object(id, request.user)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, id):
        post = self.get_object(id, request.user)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        return get_object_or_404(Post, id=id, user=user)
    def delete(self, request, id):
        post = self.get_object(id, request.user)
        post.delete()
        return Response({'message':"deleted succesfully"},status=status.HTTP_204_NO_CONTENT)'''


class AddTagToPostView(APIView):

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        tags = TagSerializer(post.tags.all(), many=True).data
        return Response({'tags': tags}, status=status.HTTP_200_OK)

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        tag_data = request.data
        tag, created = Tag.objects.get_or_create(name=tag_data['name'])
        post.tags.add(tag)
        return Response({'status': 'tag added'}, status=status.HTTP_200_OK)