from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from permissions import IsAdmin, IsAuthor,IsReader
from .models import Profile
from .serializer import UserSerializer, AdminSerializer, ProfileSerializer, UpdateProfileSerializer, LoginSerializer

class CreateAdminAPI(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        data = request.data.copy()

        serializer = AdminSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        admin_user = serializer.save()
        profile = Profile.objects.create(
            user=admin_user,
            gender=request.data.get("gender"),
            role = request.data.get("role"),
            phone = request.data.get("phone")
        )

        return Response({
            "message":"User created successfully",
            "user": serializer.data,
            "profile_id":profile.id 
        },status=status.HTTP_201_CREATED)
    
class CreateUserAPI(APIView):
    permission_classes=[]

    def post(self,request):
        data = request.data.copy()

        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()

        profile = Profile.objects.create(
            user=user,
            gender=request.data.get("gender"),
            role = request.data.get("role"),
            phone = request.data.get("phone")
        )

        return Response({
            "message":"User created successfully",
            "user": serializer.data,
            "profile_id":profile.id 
        },status=status.HTTP_201_CREATED)
    
class LoginAPI(APIView):
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]
        role = serializer.validated_data["role"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "role": role
        }, status=status.HTTP_200_OK)

    
class ProfileDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile_details = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile_details)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request,id):
        profile_details = get_object_or_404(Profile,id=id,is_active=True)
        serializer = UpdateProfileSerializer(profile_details, data=request.data)
        if profile_details.user == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Data Updated successfully",
                    "data": serializer.data
                })
        return Response({
            "message":"You do not have access to this profile"
        },status=status.HTTP_401_UNAUTHORIZED)    
        #return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ListUsersAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        profiles = Profile.objects.filter(is_active=True).order_by("id")
        paginator = PageNumberPagination()
        paginator.page_size = 5  
        paginated_profiles = paginator.paginate_queryset(profiles, request)
        serializer = ProfileSerializer(paginated_profiles, many=True)

        return paginator.get_paginated_response(serializer.data)
    
class DeleteUserAPI(APIView):
    permission_classes = [IsAdmin]

    def delete(self,request,id):
        profile = get_object_or_404(Profile,id=id)

        if profile.role == "admin":
            return Response("You cannot delete another admin account",status=status.HTTP_403_FORBIDDEN)

        if profile.is_active == True:
            profile.is_active = False
            profile.save()
            return Response({
                "message":"User deleted successfully"
            },status=status.HTTP_200_OK)
        return Response("Profile does not exist",status=status.HTTP_404_NOT_FOUND)
