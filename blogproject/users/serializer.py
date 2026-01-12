from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from constants import user_role, admin_role
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]

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
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("User profile not found")

        if not profile.is_active:
            raise serializers.ValidationError("User account is inactive")

        # Attach validated objects for view usage
        data["user"] = user
        data["role"] = profile.role

        return data

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ["id","user","role","gender","phone"]

    def validate_role(self, value):
        if value not in user_role:
            raise serializers.ValidationError("role should either be 'author' or 'reader' ")
        return value


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","gender","phone"]

class DeleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","gender","phone","is_active"]