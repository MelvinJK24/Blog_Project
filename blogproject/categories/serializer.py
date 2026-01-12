from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %m %Y")
    
    class Meta:
        model = Category
        fields = ["id","name", "description","created_at"]