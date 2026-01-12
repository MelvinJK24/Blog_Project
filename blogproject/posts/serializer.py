from rest_framework import serializers
from django.contrib.auth.models import User
from categories.models import Category
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    is_active = serializers.BooleanField(write_only = True)
    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long"
            )
        return value

    def validate_description(self, value):
        if len(value.strip()) < 15:
            raise serializers.ValidationError(
                "Description must be at least 15 characters long"
            )
        return value
    
    def validate_content(self, value):
        if len(value.strip()) < 50:
            raise serializers.ValidationError(
                "Content must be at least 50 characters long"
            )
        return value

