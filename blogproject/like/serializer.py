from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post
from .models import Like

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ["post"]