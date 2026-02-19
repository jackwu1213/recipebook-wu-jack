#!/usr/bin/env python
"""
Script to import recipe data from JSON files into the database.
Run this with: python manage.py shell < import_data.py
Or run: python import_data.py (after setting up Django)
"""
import os
import django
import json
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipebook.settings")
django.setup()

from ledger.models import Ingredient, Recipe, RecipeIngredient

BASE_DIR = Path(__file__).resolve().parent


def load_json_file(filename):
    """Load JSON data from file."""
    file_path = BASE_DIR / filename
    with file_path.open(encoding="utf-8") as f:
        return json.load(f)


def import_recipes():
    """Import recipes from Recipe List Context.txt"""
    data = load_json_file("Recipe List Context.txt")
    
    for recipe_data in data["recipes"]:
        recipe, created = Recipe.objects.get_or_create(name=recipe_data["name"])
        
        for ing_data in recipe_data["ingredients"]:
            # Handle typo in Recipe 2 JSON: "quanity" -> "quantity"
            quantity = ing_data.get("quantity") or ing_data.get("quanity", "")
            ingredient_name = ing_data["name"]
            
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={"quantity": quantity}
            )
    
    print(f"Imported {Recipe.objects.count()} recipes")
    print(f"Imported {Ingredient.objects.count()} ingredients")
    print(f"Imported {RecipeIngredient.objects.count()} recipe-ingredient relationships")


if __name__ == "__main__":
    import_recipes()

