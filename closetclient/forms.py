from django.contrib.auth.models import User
from django import forms
from .models import Profile, User, Item, Category

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)


class ProfileForm(forms.ModelForm):  

    class Meta:
        model = Profile
        fields = ('account_name', 'zipcode',)


class ItemForm(forms.ModelForm):

    class Meta:
        post = forms.CharField()
        model = Item
        fields = ('item_category', 'title', 'description', 'brand', 'image_path',)
