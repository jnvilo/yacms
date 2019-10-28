from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CMSUser


class CMSUserCreationForm(UserCreationForm):
    class Meta:
        model = CMSUser
        fields = ("username", "email")


class CMSUserChangeForm(UserChangeForm):
    class Meta:
        model = CMSUser
        fields = ("username", "email")
