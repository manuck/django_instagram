from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Profile
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)
    
class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        # fields = ('nickname', 'introduction', 'image')