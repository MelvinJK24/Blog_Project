from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from permissions import IsAdmin, IsAuthor, IsReader
from posts.models import Post
from .models import Comment
from .serializer import CommentSerializer

class CreateCommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        post_id = request.data.get("post")
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if post.is_published == False:
            return Response({
                "message": "Post unavailable"
            },status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(writer = request.user,post=post)
            return Response({
                "message": "Comment created successfully",
                "comment": serializer.data.get("comment"),
                "post": serializer.data.get("post")
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ListCommentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        post_id = get_object_or_404(Post,id=id)
        comments = Comment.objects.filter(post = post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EditCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,id):
        comment  = get_object_or_404(Comment, id = id)
        data = request.data.copy()
        data.pop("post", None)
        data.pop("writer", None)
        
        if comment.writer == request.user:        
            serializer = CommentSerializer(comment, data=data, partial=True)
             
            if serializer.is_valid():               
                serializer.save(is_edited =True)
                return Response({
                    "message":"Comment edited successfully",
                    "data": serializer.data
                },status=status.HTTP_200_OK)
        
        return Response({
            "message":"Only the comment author can edit the comment"
        }, status=status.HTTP_403_FORBIDDEN)