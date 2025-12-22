from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateCategoryAPI, ListCategoryAPI, UpdateCategoryAPI, DeleteCategoryAPI

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createcategory', CreateCategoryAPI.as_view()),
    path('listcategory',ListCategoryAPI.as_view()),
    path('updatecategory/<int:id>', UpdateCategoryAPI.as_view()),
    path('deletecategory/<int:id>',DeleteCategoryAPI.as_view())
]