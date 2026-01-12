from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from categories.models import Category
from permissions import IsAdmin, IsAuthor, IsReader
from posts.models import Post
from .serializer import DraftSerializer

class ListDraftsAPI(APIView):
    permission_classes = [IsAuthor]
    def get(self, request):
        drafts = Post.objects.filter(is_published=False,is_active=True,author = request.user)
        serializer = DraftSerializer(drafts,many=True)  
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class PublishDraftAPI(APIView):
    permission_classes = [IsAuthor]
    def put(self, request,id):
        post = get_object_or_404(Post, id=id,is_active=True)
        serializer = DraftSerializer(post)
        if not post.author == request.user:
            return Response({
                "message":"Post unavailable"
                },status=status.HTTP_401_UNAUTHORIZED)
        
        if post.is_published == False:
            post.is_published = True
            post.save()
            return Response({
                "message":"Post published",
                "data":serializer.data
            })
        
        return Response({
            "message":"Post is already published"
        },status=status.HTTP_400_BAD_REQUEST)

class UnpublishPostAPI(APIView):
    permission_classes= [IsAuthor]

    def put(self,request,id):
        post = get_object_or_404(Post,id=id, is_active=True)
        serializer = DraftSerializer(post)
        if not post.author == request.user:
            return Response({
                "message":"You are not the author"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if post.is_published == True:
            post.is_published = False
            post.save()
            return Response({
                "message":"Post unpublished",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        
        return Response({
            "message":"Post is not published yet."
        },status=status.HTTP_400_BAD_REQUEST)