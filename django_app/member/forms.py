from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput, required=True)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, required=True)
    img_profile = forms.ImageField(required=True)