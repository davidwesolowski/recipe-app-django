from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<uuid:id>', views.recipe, name='recipe'),
    path('create/', views.create_recipe, name='create-recipe'),
    path('delete/<uuid:id>', views.delete_recipe, name='delete-recipe'),
    path('edit/<uuid:id>', views.edit_recipe, name='edit-recipe'),
    path('profile/', views.profile, name='profile')
]