from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Users, Recipes
from .forms import CreateRecipeForm, EditProfile


# Create your views here.


def index(response):
    all_recipes = []
    users = Users.objects.all()
    for user in users:
        for recipe in user.recipes_set.all():
            all_recipes.append({'author': user.name, 'recipe': {"ID": recipe.ID, "title": recipe.title, 'imageUrl': recipe.imageUrl}})
    return render(response, 'main/recipes-list.html', {'all_recipes': all_recipes})


def recipe(response, id):
    try:
        recipe = Recipes.objects.get(ID=id)
        user = Users.objects.get(ID=recipe.userID.ID)
        role = str(response.user.rola)
        return render(response, 'main/recipe.html', {'userInfo': user, 'role': role, 'recipe': recipe, 'error': ''})
    except:
        return render(response, 'main/not-found.html', {'error': 'Nie ma takiego przepisu!'})


@login_required
def delete_recipe(response, id):
    try:
        recipe = Recipes.objects.get(ID=id)
        if response.user and response.user.ID == recipe.userID.ID:
            recipe.delete()
        return HttpResponseRedirect('/')
    except:
        return render(response, 'main/not-found.html', {'error': 'Taki przepis nie istnieje!'})


@login_required
def create_recipe(response):
    if response.method == 'POST':
        form = CreateRecipeForm(response.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            imageUrl = form.cleaned_data['imageUrl']
            user = Users.objects.get(ID=response.user.ID)
            recipe = user.recipes_set.create(title=title, description=description, imageUrl=imageUrl)
            print(recipe.ID)
            user.save()
            return HttpResponseRedirect('/%s' % recipe.ID)
    else:
        form = CreateRecipeForm()
    return render(response, 'main/create-recipe.html', {'form': form})


@login_required
def edit_recipe(response, id):
    if response.POST:
        form = CreateRecipeForm(response.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            imageUrl = form.cleaned_data['imageUrl']
            recipe = Recipes.objects.get(ID=id)
            recipe.title = title
            recipe.description = description
            recipe.imageUrl = imageUrl
            recipe.save()
            return HttpResponseRedirect('/%s' % recipe.ID)
    else:
        try:
            recipe = Recipes.objects.get(ID=id)
            if response.user and response.user.ID == recipe.userID.ID:
                form = CreateRecipeForm(initial={
                    'title': recipe.title, 'description': recipe.description, 'imageUrl': recipe.imageUrl
                })
                return render(response, 'main/edit-recipe.html', {'form': form, 'recipe': recipe})
            else:
                return HttpResponseRedirect('/')
        except:
            return render(response, 'main/not-found.html', {'error': 'Taki przepis nie istnieje!'})


@login_required
def profile(response):
    if response.method == 'POST':
        form = EditProfile(response.POST)
        if form.is_valid():
            try:
                current_user = Users.objects.get(ID=response.user.ID)
                name = form.cleaned_data['name'].lower()
                password = form.cleaned_data['password']
                successName = ''
                succcessPassword = ''
                if len(name) > 0 and name != current_user.name:
                    current_user.name = name
                    successName = 'Nazwa zmieniona pomyślnie\n'
                if len(password) > 0:
                    current_user.set_password(password)
                    update_session_auth_hash(response, current_user)
                    succcessPassword = 'Hasło zmienione pomyślnie'
                current_user.save()
                return render(response, 'main/profile.html', {'form': form, 'successName': successName, 'succcessPassword': succcessPassword})
            except:
                return render(response, 'main/not-found.html', {'error': 'Taki użytkownik nie istnieje!'})
        else:
            return render(response, 'main/profile.html', {'form': form})
    else:
        form = EditProfile(initial={'email': response.user.email, 'name': response.user.name})
        return render(response, 'main/profile.html', {'form': form})

