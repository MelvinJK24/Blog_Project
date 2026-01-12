from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateCategoryAPI, ListCategoryAPI, UpdateCategoryAPI, DeleteCategoryAPI

urlpatterns = [
    path('createcategory', CreateCategoryAPI.as_view()),
    path('listcategory',ListCategoryAPI.as_view()),
    path('updatecategory/<int:id>', UpdateCategoryAPI.as_view()),
    path('deletecategory/<int:id>',DeleteCategoryAPI.as_view())
]