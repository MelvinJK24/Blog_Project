from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreatePostAPI, ListPostAPI, UpdatePostAPI, MyPostsAPI, DeletePostAPI, ViewPostAPI

urlpatterns = [
    path('createpost', CreatePostAPI.as_view()),
    path('listposts',ListPostAPI.as_view()),
    path('updateposts/<int:id>', UpdatePostAPI.as_view()),
    path('myposts',MyPostsAPI.as_view()),
    path('deletepost/<int:id>',DeletePostAPI.as_view()),
    path('viewpost/<int:id>',ViewPostAPI.as_view())
]