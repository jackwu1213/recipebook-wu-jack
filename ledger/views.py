from django.shortcuts import render, get_object_or_404

from .models import Recipe


def recipe_list(request):
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "ledger/recipe_list.html", context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {"recipe": recipe}
    return render(request, "ledger/recipe_detail.html", context)
