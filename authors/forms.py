'''
from socket import fromshare
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        })
                                )
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'password'
                  ]

        help_texts = {
            'email': 'Email must be valid'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
            
        }

'''
