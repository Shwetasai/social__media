from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('Users/', include('Users.urls')),
    path('api/Users/', include('Users.urls')),
    path('api/followers/', include('followers.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/comments/',include('comments.urls')),
    
]
    
    
