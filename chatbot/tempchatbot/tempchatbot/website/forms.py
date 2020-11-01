from django import forms

from .models import *

'''
class userForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'password')
'''


class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
