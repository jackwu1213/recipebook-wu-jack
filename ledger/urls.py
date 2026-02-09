from django.urls import path

from . import views

app_name = "ledger"

urlpatterns = [
    path("recipes/list", views.recipe_list, name="recipe_list"),
    path("recipe/1", views.recipe_one, name="recipe_one"),
    path("recipe/2", views.recipe_two, name="recipe_two"),
]


