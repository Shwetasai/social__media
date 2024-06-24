from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import CustomUser
from .serializers import CustomUserSerializer,UserLoginSerializer,TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.conf import settings
import base64
import json
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import AccessToken

class CustomUserCreateView(APIView):

    def post(self, request, *args, **kwargs): 
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not email or not username or not password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            
            # Encode user data for email verification
        user_data = {
                'email': email,
                'username': username,
                'password': password,
            }
        encoded_user_data = base64.urlsafe_b64encode(json.dumps(user_data).encode()).decode()
        print("Encoded User Data:", encoded_user_data)

         
            # Send verification email
        verification_link = f"{request.scheme}://{request.get_host()}/api/Users/verify/?data={encoded_user_data}"
        print(f"Verification Link: {verification_link}")
        send_mail(
                subject='Verify your email',
                message=f"Click the link to verify your email and complete registration: {verification_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        print(f"Verification email sent to {email}")

        return Response({
                "message": "Verification email sent. Please check your email to complete registration.",
                'username': username
            }, status=status.HTTP_201_CREATED)
    



    def get(self, request, *args, **kwargs):
        encoded_user_data = request.query_params.get('data')
        print(f"Encoded User Data from URL: {encoded_user_data}")
        if not encoded_user_data:
            
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)

        # Decode user data
        decoded_user_data = json.loads(base64.urlsafe_b64decode(encoded_user_data).decode())
        email = decoded_user_data["email"]
        username = decoded_user_data["username"]
        password = decoded_user_data["password"]
       

        # Save user data to database
        user = CustomUser.objects.filter(email=email).exists()
        if not user:
            user = CustomUser.objects.create_user(email=email, username=username, password=password)
        user.is_email_verified = True
        user.save()
        return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):

    def post(self, request, *args, **kwargs):
        
        # Handle user login functionality
        login_serializer = UserLoginSerializer(data=request.data)
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            access_token = AccessToken.for_user(user)
            return Response({
                'access': str(access_token),
                'email':user.email
            }, status=status.HTTP_200_OK)
        
        # If both serializers are invalid, return errors
        errors = {}
        if token_serializer.errors:
            errors['token_errors'] = token_serializer.errors
        if login_serializer.errors:
            errors['login_errors'] = login_serializer.errors
        
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


