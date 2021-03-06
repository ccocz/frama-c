from django.urls import path, include

from . import views

app_name = "framac"

urlpatterns = [
    path('', views.index, name='index'),
    path('add-file/', views.get_file, name='add-file'),
    path('add-directory/', views.get_directory, name='add-directory'),
    path('files/<int:file_id>', views.file_index, name='file'),
    path('files/delete/<int:file_id>', views.delete_file, name='file_delete'),
    path('files/reprove/<int:file_id>', views.reprove, name='reprove'),
    path('directories/<int:directory_id>', views.directory_index, name='directory'),
    path('directories/delete/<int:directory_id>', views.delete_directory, name='directory_delete'),
    path('tabs/prover', views.prover_tab, name='prover'),
    path('tabs/vc', views.vc_tab, name='vc'),
    path('tabs/result/<int:file_id>', views.result, name='result'),
    path('users/', include('django.contrib.auth.urls'))
]
