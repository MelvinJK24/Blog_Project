from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):

    def has_permission(self,request,views):
        return request.user.is_authenticated and request.user.profile.role == "admin"
    
class IsAuthor(BasePermission):

    def has_permission(self,request,views):
        return request.user.is_authenticated and request.user.profile.role == "author"
    
class IsReader(BasePermission):

    def has_permission(self,request,views):
        return request.user.is_authenticated and request.user.profile.role == "reader"