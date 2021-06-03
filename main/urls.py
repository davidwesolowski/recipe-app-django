from django.urls import path

from . import views

urlpatterns = [
    # path('<int:id>', views.index, name='index'),
    path('', views.index, name='home'),
    path('<int:id>', views.recipe, name='recipe'),
    path('create/', views.create_recipe, name='create-recipe'),
    path('delete/<int:id>', views.delete_recipe, name='delete-recipe'),
    path('edit/<int:id>', views.edit_recipe, name='edit-recipe'),
    path('profile/', views.profile, name='profile')
]