from django import forms
from .models import Post, Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('post', )
        widgets = {
            'file': forms.FileInput(attrs={'multiple': True}),
        }