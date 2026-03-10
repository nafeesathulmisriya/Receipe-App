from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [

      # PUBLIC PAGE (first page)
    path('', views.index, name='index'),

    # HOME PAGE
    path('home/', views.home, name='home'),
    # Auth & home

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    # Recipe detail
    path('details/<int:id>/', views.recipe_detail, name='recipe_detail'),

    # Category page
    path('category/<int:category_id>/', views.category_recipes, name='category_recipes'),

    # Recipe management
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/edit/<int:id>/', views.edit_recipe, name='edit_recipe'),
    path('recipes/delete/<int:id>/', views.delete_recipe, name='delete_recipe'),
]
