from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.TextField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active =models.BooleanField(default=True)

    def __str__(self):
        return self.name