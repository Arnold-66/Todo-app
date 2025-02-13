from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('tasklist', views.tasklist, name= 'tasklist'),
    path('task/update/<int:task_id>/', views.updatetask, name='updatetask'),
    path('delete/<int:task_id>/', views.deletetask, name='deletetask'),

    
]
