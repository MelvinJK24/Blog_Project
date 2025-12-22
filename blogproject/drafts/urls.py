from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ListDraftsAPI, PublishDraftAPI, UnpublishPostAPI
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('listdrafts', ListDraftsAPI.as_view()),
    path('publishdraft/<int:id>',PublishDraftAPI.as_view()),
    path('unpublishpost/<int:id>',UnpublishPostAPI.as_view())
]