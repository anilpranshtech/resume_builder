from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('select_theme/', views.select_theme, name='select_theme'),
    path('create/', views.create_resume, name='create_resume'),
    path('edit/<int:id>/', views.edit_resume, name='edit_resume'),
    path('list/', views.resume_list, name='resume_list'),
    path('detail/<int:id>/', views.resume_detail, name='resume_detail'),
    path('delete/<int:id>/', views.resume_delete, name='resume_delete'),
]