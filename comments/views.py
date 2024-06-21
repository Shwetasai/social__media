from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, Reply
from .serializers import CommentSerializer, ReplySerializer

class CommentCreateView(APIView):
    def post(self, request, post_id):
        data = request.data.copy()
        data['post'] = post_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyCreateView(APIView):  
    
    def post(self, request, comment_id):
        data = request.data.copy()
        data['comment'] = comment_id
        serializer = ReplySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)