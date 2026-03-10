from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    ingredients = models.TextField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
