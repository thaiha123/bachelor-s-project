from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class signup_form(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",]

class user_edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ["password1", "password2"]

class profile_edit_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic", "work_at", "intro"]