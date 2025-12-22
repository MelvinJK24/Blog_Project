from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from categories.models import Category
from permissions import IsAdmin, IsAuthor, IsReader
from .models import Post
from .serializer import PostSerializer

class CreatePostAPI(APIView):
    permission_classes = [IsAuthor]

    def post(self, request):
        
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "message":"Blog created successfully",
                "data": serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListPostAPI(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(is_published =True)
        
        category = request.GET.get("category")
        if category:
            posts = posts.filter(category__name__icontains=category)

        search = request.GET.get("search")
        if search:
            posts  =  posts.filter(
                Q(title__icontains=search) | Q(category__name__icontains=search)
            )
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ViewPostAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        post = get_object_or_404(Post,id=id)

        if not post.is_active:
            return Response({
                "Error":"Post not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if  post.is_published == False and (request.user.profile.role != "admin" and post.author != request.user):
                return Response({"message":"Post unavailable"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)

class MyPostsAPI(APIView):
    def get(self, request):
        posts = Post.objects.filter(is_active = True, author = request.user)
        #posts = posts.filter(posts.author == request.author)
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UpdatePostAPI(APIView):
    permission_classes = [IsAdmin | IsAuthor]

    def put(self, request, id):
        post = get_object_or_404(Post, id=id,is_active=True)
        if post.author == request.user:
            serializer = PostSerializer(post, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                "message" : "Post updated successfully",
                "data" : serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)
        
class DeletePostAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request,id):
        post = get_object_or_404(Post,id=id)
        if post.author == request.user:
            post.is_active = False
            post.save()

            return Response({"message":"Post deleted successfully"},status=status.HTTP_200_OK)
        
        if request.user.profile.role == "admin":
            post.is_active = False
            post.save()

            return Response({"message":"Post deleted successfully"},status=status.HTTP_200_OK)
        
        return Response({"message":"You don't have access to delete the post"},status=status.HTTP_400_BAD_REQUEST)