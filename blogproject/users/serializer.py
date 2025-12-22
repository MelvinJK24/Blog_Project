from rest_framework import serializers
from django.contrib.auth.models import User
from constants import user_role, admin_role
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email","role"]

    def validate_role(self, value):
        if value not in user_role:
            raise serializers.ValidationError("role should either be 'author' or 'reader' ")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email", "")
        )
        user.save()
        
        return user
    
class AdminSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields= ["id", "username", "password", "first_name", "last_name", "email","role"]

    def validate_role(self, value):
        if value not in admin_role:
            raise serializers.ValidationError("role should be 'admin'")
        return value

    def create(self, validated_data):
        admin = User.objects.create_user(
            username =validated_data["username"],
            password = validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email", "")
        )
        
        admin.save()
        return admin
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ["id","user","role","gender","phone"]

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","gender","phone"]

class DeleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","gender","phone","is_active"]