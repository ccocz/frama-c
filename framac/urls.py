from django.urls import path

from . import views

app_name = "framac"

urlpatterns = [
    path('', views.index, name='index'),
    path('add-file/', views.get_file, name='add-file'),
    path('add-directory/', views.get_directory, name='add-directory')
]
