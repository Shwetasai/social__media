from django.urls import path
from .views import CustomUserCreateView,UserLoginView#,EchoAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('create/', CustomUserCreateView.as_view(), name='create_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    
    
]

'''path('echo/', EchoAPIView.as_view(), name='echo_api'),'''