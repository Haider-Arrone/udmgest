from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite o nome de usuário')
        add_placeholder(self.fields['password'], 'Digite a senha')

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
