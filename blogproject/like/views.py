from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from permissions import IsAdmin, IsAuthor, IsReader
from posts.models import Post
from .models import Like
from .serializer import LikeSerializer

class LikeAPI(APIView):
    permission_classes = [IsAuthor | IsReader]

    def post(self, request):
        post_id = request.data.get("post")
        post = get_object_or_404(Post,id=post_id)
        
        if not post.is_published:
                
                return Response({
                    "message":"Post unavailable"
                }, status=status.HTTP_404_NOT_FOUND)
        
        like = Like.objects.filter(user = request.user,post=post)
        if like.exists():
            if post.like_count>0:
                like.delete()
                post.like_count = post.like_count - 1
                post.save()
                return Response({
                "message":"Post unliked"
            },status=status.HTTP_200_OK)

        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():          
            post.like_count = post.like_count + 1
            post.save()
            serializer.save(user = request.user)

            return Response({"message":"Post liked successfully"})
                         
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LikeCountAPI(APIView):
    permission_classes = [IsAuthor | IsReader]

    def get(self, request,id):
        post = get_object_or_404(Post,id=id)
        return Response({
             "Likes":post.like_count},
            status=status.HTTP_200_OK)