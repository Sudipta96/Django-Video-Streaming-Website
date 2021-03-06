from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models import Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    website = forms.URLField(required=False,
                             widget=forms.TextInput(attrs={
                             'placeholder': 'https://'}))
    class Meta:
        model = Profile
        fields = ['channel_name','profile_pic','description','website']
