from django.db import models
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    content = models.TextField()
    
    def __str__(self):
        return f'Post : {self.pk}'
    
    def get_absolute_url(self):
        return reverse('posts:detail', args=[self.pk])