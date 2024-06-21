from django.urls import path
from .views import PostCreateAPIView,AddTagToPostView,PostmanageAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post_create'),
    path('add_tag/<int:id>/', AddTagToPostView.as_view(), name='add-tag-to-post'),
    path('manage/<int:id>/',PostmanageAPIView.as_view(), name='manage_post'),


]