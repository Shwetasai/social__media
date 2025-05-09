from django.urls import path
from .views import CustomUserCreateView,UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('create/', CustomUserCreateView.as_view(), name='create_user'),
    path('verify/', CustomUserCreateView.as_view(), name='verify_user'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

'''path('echo/', EchoAPIView.as_view(), name='echo_api'),'''