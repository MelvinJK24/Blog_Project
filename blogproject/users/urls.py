from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateAdminAPI, CreateUserAPI, ProfileDetailsAPI, UpdateProfileAPI, ListUsersAPI, DeleteUserAPI, LoginAPI
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createadmin', CreateAdminAPI.as_view()),
    path('createuser', CreateUserAPI.as_view()),
    path('profiledetails',ProfileDetailsAPI.as_view()),
    path('updateprofile/<int:id>', UpdateProfileAPI.as_view()),
    path('listusers',ListUsersAPI.as_view()),
    path('deleteuser/<int:id>',DeleteUserAPI.as_view()),
    path('login/',LoginAPI.as_view(),name="login")
]