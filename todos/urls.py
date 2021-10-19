from django.contrib import admin
from django.urls import path
from todos import views

urlpatterns = [
    path('', views.TodosAPIView.as_view(),name='todos'),
    path('<int:id>', views.TodoDetailAPIView.as_view(),name='todo'),
    # path('create/', views.CreateTodoAPIView.as_view(),name='create-todo'),
    # path('list/', views.TodoListAPIView.as_view(),name='list-todo'),
]
