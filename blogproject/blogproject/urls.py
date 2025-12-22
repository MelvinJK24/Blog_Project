from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('posts/',include('posts.urls')),
    path('comments/',include('comments.urls')),
    path('categories/',include('categories.urls')),
    path('likes/',include('like.urls')),
    path('drafts/',include('drafts.urls'))
]