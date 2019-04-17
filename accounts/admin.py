from django.contrib import admin
# from .models import User
from django.contrib.auth import get_user_model
from .models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'introduction', 'user_id',)
    
admin.site.register(get_user_model())
admin.site.register(Profile, ProfileAdmin)