from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from permissions import IsAdmin, IsAuthor, IsReader

from .models import Category
from .serializer import CategorySerializer

class CreateCategoryAPI(APIView):
    permission_classes= [IsAdmin]

    def post(self, request):
        serializer = CategorySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Category created successfully",
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCategoryAPI(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(is_active=True).order_by("id")
        paginator = PageNumberPagination()
        paginator.page_size = 5  
        paginated_categories = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(paginated_categories, many=True)
        return paginator.get_paginated_response(serializer.data)
        
class UpdateCategoryAPI(APIView):
    permission_classes = [IsAdmin]

    def put(self,request,id):
        category = get_object_or_404(Category,id=id)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Category updated successfully",
                "data": serializer.data
            },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DeleteCategoryAPI(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request,id):
        category= get_object_or_404(Category,id=id)
        
        category.is_active = False
        category.save()

        return Response(
            {"message":"Category deleted successfully"}, 
            status=status.HTTP_200_OK
        )