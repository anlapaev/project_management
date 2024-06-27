from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/new/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:pk>/add_member/', views.project_add_member, name='project_add_member'),
    path('project/<int:project_pk>/remove_member/<int:user_pk>/', views.project_remove_member, name='project_remove_member'),
    path('project/<int:project_pk>/task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:task_pk>/comment/', views.add_comment_to_task, name='add_comment_to_task'),
    path('register/', views.register, name='register'),
]

