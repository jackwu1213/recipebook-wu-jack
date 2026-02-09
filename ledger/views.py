from pathlib import Path
import json

from django.shortcuts import render


BASE_DIR = Path(__file__).resolve().parent.parent


def _load_json_from_file(filename):
    file_path = BASE_DIR / filename
    with file_path.open(encoding="utf-8") as file_handle:
        return json.load(file_handle)


def recipe_list(request):
    context = _load_json_from_file("Recipe List Context.txt")
    return render(request, "ledger/recipe_list.html", context)


def recipe_one(request):
    context = _load_json_from_file("Recipe 1.txt")
    return render(request, "ledger/recipe_detail.html", context)


def recipe_two(request):
    context = _load_json_from_file("Recipe 2.txt")
    return render(request, "ledger/recipe_detail.html", context)
