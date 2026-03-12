from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RecipeForm, RecipeImageForm
from .models import Profile, Recipe


def recipe_list(request):
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "ledger/recipe_list.html", context)


@login_required(login_url="ledger:login")
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {"recipe": recipe}
    return render(request, "ledger/recipe_detail.html", context)


@login_required(login_url="ledger:login")
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            profile, _ = Profile.objects.get_or_create(
                user=request.user,
                defaults={
                    "name": request.user.get_username(),
                    "short_bio": "",
                },
            )
            recipe = form.save(commit=False)
            recipe.author = profile
            recipe.save()
            return redirect("ledger:recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm()

    context = {"form": form}
    return render(request, "ledger/recipe_form.html", context)


@login_required(login_url="ledger:login")
def recipe_add_image(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = RecipeImageForm(request.POST, request.FILES)
        if form.is_valid():
            recipe_image = form.save(commit=False)
            recipe_image.recipe = recipe
            recipe_image.save()
            return redirect("ledger:recipe_detail", pk=recipe.pk)
    else:
        form = RecipeImageForm()

    context = {
        "form": form,
        "recipe": recipe,
    }
    return render(request, "ledger/recipe_image_form.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("ledger:recipe_list")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "ledger/login.html")


def user_logout(request):
    logout(request)
    return redirect("ledger:login")


def password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            try:
                from django.contrib.auth.models import User
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully. Please login with your new password.")
                return redirect("ledger:login")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
    
    return render(request, "ledger/password_reset.html")
