from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Recipe

from .forms import RecipeForm


# ================= INDEX =================
def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', {'recipes': recipes})

# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipes:home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'recipes/login.html')


# ================= SIGNUP =================
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if not username or not password or not confirm:
            messages.error(request, "All fields are required")
            return redirect('recipes:signup')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('recipes:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('recipes:signup')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully")
        return redirect('recipes:login')

    return render(request, 'recipes/signup.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('recipes:login')


# ================= HOME (CATEGORY FILTER WORKS HERE) =================
@login_required
def home(request):
    categories = Category.objects.all()
    return render(request, 'recipes/home.html', {
        'categories': categories
    })


# ================= RECIPE DETAIL =================
@login_required(login_url='recipes:login')
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    related_recipes = Recipe.objects.filter(
        category=recipe.category
    ).exclude(id=recipe.id)[:3]

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'related_recipes': related_recipes
    })

# ================= CATEGORY PAGE (OPTIONAL BUT CLEAN) =================
@login_required
def category_recipes(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Only recipes with a valid ID
    recipes = Recipe.objects.filter(category=category).exclude(id__isnull=True)

    return render(request, 'recipes/category_recipes.html', {
        'category': category,
        'recipes': recipes
    })




# LIST RECIPES (with add button)
@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(created_by=request.user)
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


# ADD RECIPE
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})


# EDIT RECIPE
@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, created_by=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form})


# DELETE RECIPE
@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, created_by=request.user)
    recipe.delete()
    return redirect('recipes:recipe_list')



def about(request):
    return render(request, 'recipes/about.html')


from django.db.models import Q
from .models import Recipe

def recipe_list(request):
    query = request.GET.get('q')

    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        recipes = Recipe.objects.all()

    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes
    })