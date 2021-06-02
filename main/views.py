from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Users, Recipes
from .forms import CreateRecipeForm


# Create your views here.


def index(response):
    all_recipes = []
    users = Users.objects.all()
    for user in users:
        for recipe in user.recipes_set.all():
            all_recipes.append({'author': user.name, 'recipe': {"id": recipe.id, "title": recipe.title, 'imageurl': recipe.imageurl}})
    for user in users:
        for recipe in user.recipes_set.all():
            all_recipes.append({'author': user.name, 'recipe': {"id": recipe.id, "title": recipe.title, 'imageurl': recipe.imageurl}})
    return render(response, 'main/recipes-list.html', {'all_recipes': all_recipes})


def home(response):
    return render(response, 'main/home.html', {})


def recipe(response, id):
    try:
        recipe = Recipes.objects.get(id=id)
        user = Users.objects.get(id=recipe.userId.id)
        return render(response, 'main/recipe.html', {'user': user, 'recipe': recipe, 'error': ''})
    except:
        return render(response, 'main/not-found.html', {'error': 'Nie ma takiego przepisu!'})


def delete_recipe(response, id):
    try:
        recipe = Recipes.objects.get(id=id)
        recipe.delete()
        return HttpResponseRedirect('/')
    except:
        return render(response, 'main/not-found.html', {'error': 'Taki przepis nie istnieje!'})


def create_recipe(response):
    if response.method == 'POST':
        form = CreateRecipeForm(response.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            imageUrl = form.cleaned_data['imageUrl']
            user = Users.objects.get(id=1)
            recipe = user.recipes_set.create(title=title, description=description, imageUrl=imageUrl)
            user.save()
            return HttpResponseRedirect('/%i' % recipe.id)
    else:
        form = CreateRecipeForm()
    return render(response, 'main/create-recipe.html', {'form': form})


def edit_recipe(response, id):
    if response.POST:
        form = CreateRecipeForm(response.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            imageUrl = form.cleaned_data['imageUrl']
            recipe = Recipes.objects.get(id=id)
            recipe.title = title
            recipe.description = description
            recipe.imageUrl = imageUrl
            recipe.save()
            return HttpResponseRedirect('/%i' % recipe.id)
    else:
        try:
            recipe = Recipes.objects.get(id=id)
            form = CreateRecipeForm(initial={
                'title': recipe.title, 'description': recipe.description, 'imageUrl': recipe.imageUrl
            })
            return render(response, 'main/edit-recipe.html', {'form': form, 'recipe': recipe})
        except:
            return render(response, 'main/not-found.html', {'error': 'Taki przepis nie istnieje!'})

