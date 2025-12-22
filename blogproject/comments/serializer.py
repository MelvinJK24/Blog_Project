from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        #read_only_fields = ["post"]