from django.urls import path
from .views import CustomFollowUserView

urlpatterns = [
    path('follow/', CustomFollowUserView.as_view(), name='follow_user'),
]