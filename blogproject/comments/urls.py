from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateCommentAPI, ListCommentsAPI, EditCommentAPI

urlpatterns = [
    path('createcomment', CreateCommentAPI.as_view()),
    path('listcomments/<int:id>',ListCommentsAPI.as_view()),
    path('editcomment/<int:id>',EditCommentAPI.as_view())
]