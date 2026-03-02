from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Recipe


def recipe_list(request):
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "ledger/recipe_list.html", context)


@login_required(login_url="ledger:login")
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {"recipe": recipe}
    return render(request, "ledger/recipe_detail.html", context)


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
