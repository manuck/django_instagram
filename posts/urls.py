from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.list, name='list'),
    path('new/', views.new, name='new'),
    path('detail/<int:post_pk>/', views.detail, name='detail'),
    path('delete/<int:post_pk>/', views.delete, name='delete'),
    path('update/<int:post_pk>/', views.update, name='update'),
]