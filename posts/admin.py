from django.contrib import admin
from .models import Post, Image
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'content',]

admin.site.register(Post, PostAdmin)
admin.site.register(Image)