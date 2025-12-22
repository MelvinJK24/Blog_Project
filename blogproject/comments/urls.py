from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateCommentAPI, ListCommentsAPI, EditCommentAPI

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createcomment', CreateCommentAPI.as_view()),
    path('listcomments/<int:id>',ListCommentsAPI.as_view()),
    path('editcomment/<int:id>',EditCommentAPI.as_view())
]