from django import forms
from .models import User, GeneralData

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["email", "password"]

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ["email", "password"]

class GeneralDataForm(forms.ModelForm):

    class Meta:
        model = GeneralData
        fields = "__all__"

