from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.list, name='list'),
    path('new/', views.new, name='new'),
    path('detail/<int:post_pk>/', views.detail, name='detail'),
    path('delete/<int:post_pk>/', views.delete, name='delete'),
    path('update/<int:post_pk>/', views.update, name='update'),
    path('like/<int:post_pk>/', views.like, name='like'),
    path('<int:post_pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name="comments_delete"),
]