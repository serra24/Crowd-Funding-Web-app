from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username','email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    password1 = forms.CharField(
                widget=forms.PasswordInput(attrs={'class': 'form-control',"name": "Pasword",}),label = "Pasword"
            )
    password2 = forms.CharField(
                widget=forms.PasswordInput(attrs={'class': 'form-control',"name": "Repeat your password",}),label = "Repeat your password"
            )
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username' ,'first_name','last_name']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ['username' ,'first_name','last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number' , 'addres','image']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'addres': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }