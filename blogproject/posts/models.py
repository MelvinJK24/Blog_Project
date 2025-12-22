from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

class Post(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title