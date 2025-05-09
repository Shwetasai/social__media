
from django.urls import path
from .views import CommentCreateView, ReplyCreateView

urlpatterns = [
    path('comment/<int:post_id>/', CommentCreateView.as_view(), name='comment-create'),
    path('replies/<int:comment_id>/', ReplyCreateView.as_view(), name='reply-create'),
]