from django.urls import path

from . import views

app_name = "ledger"

urlpatterns = [
    path("recipes/list", views.recipe_list, name="recipe_list"),
    path("recipe/<int:pk>", views.recipe_detail, name="recipe_detail"),
]
