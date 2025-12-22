from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)