from django.contrib import admin

from .models import Ingredient, Recipe, RecipeImage, RecipeIngredient, Profile


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, RecipeImageInline]
    list_display = ["name", "author", "created_on", "updated_on"]
    search_fields = ["name"]
    list_filter = ["author", "created_on"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["recipe", "ingredient", "quantity"]
    list_filter = ["recipe", "ingredient"]


@admin.register(RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = ["recipe", "description"]
    list_filter = ["recipe"]
    search_fields = ["recipe__name", "description"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    search_fields = ["name", "user__username"]
