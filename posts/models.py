from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    
    # image = models.ImageField()
    @property
    def like_count(self):
        return self.like_users.count()
    
    def __str__(self):
        return f'Post : {self.pk}'
    
    def get_absolute_url(self):
        return reverse('posts:detail', args=[self.pk])
        
class Image(models.Model):
    file = models.ImageField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    