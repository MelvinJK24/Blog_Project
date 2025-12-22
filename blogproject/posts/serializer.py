from rest_framework import serializers
from django.contrib.auth.models import User
from categories.models import Category
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'