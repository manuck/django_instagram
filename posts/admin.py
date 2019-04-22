from django.contrib import admin
from .models import Post, Image, Comment, Hashtag
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'content',]

class HashtagAdmin(admin.ModelAdmin):
    list_display = ['pk','content']

admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Hashtag, HashtagAdmin)