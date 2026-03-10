from django.contrib import admin
from .models import Category, Recipe

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'cooking_time', 'created_by', 'created_at']
    list_filter = ['category', 'created_by']
    search_fields = ['title', 'description']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
