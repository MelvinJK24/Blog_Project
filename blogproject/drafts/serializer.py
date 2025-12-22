from rest_framework import serializers
from posts.models import Post

class DraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id","title","category","description","content","created_at"]