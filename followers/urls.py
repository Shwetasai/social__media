from django.urls import path
from .views import CustomFollowUserView,FollowersListView,FollowingListView

urlpatterns = [
    path('follow/', CustomFollowUserView.as_view(), name='follow_user'),
    path('followers/<int:id>/', FollowersListView.as_view(), name='user-followers'),
    path('following/<int:id>/', FollowingListView.as_view(), name='user-following'),

]