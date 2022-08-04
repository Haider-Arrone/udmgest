from socket import fromshare
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
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
            
        }

