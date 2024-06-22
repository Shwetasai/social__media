from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import CustomUser
from .serializers import CustomUserSerializer,UserLoginSerializer,TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomUserCreateView(APIView):

    def post(self, request, *args, **kwargs): 
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not email or not username or not password:
            return Response({'error':'all fields are require.'},status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error':'username already exists.'},status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error':'email already exists.'},status=status.HTTP_400_BAD_REQUEST)

        serializer=CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


from rest_framework_simplejwt.tokens import AccessToken

class UserLoginView(APIView):
        
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            access_token = AccessToken.for_user(user)
            return Response({
                'access': str(access_token),
            })
        else:
            print("serializer errors", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




'''from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class EchoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve and return the payload
        payload = request.data
        return Response(payload)'''