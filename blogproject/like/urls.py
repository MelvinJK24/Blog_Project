from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LikeAPI, LikeCountAPI

urlpatterns = [
    path('like', LikeAPI.as_view()),
    path('likecounts/<int:id>', LikeCountAPI.as_view())
]