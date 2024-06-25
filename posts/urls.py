from django.urls import path
from .views import PostCreateAPIView,PostManageAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post_create'),
    path('manage/<int:id>/',PostManageAPIView.as_view(), name='manage-post'),


]

