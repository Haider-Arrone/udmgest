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




class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite o nome de usuário')
        add_placeholder(self.fields['email'], 'Digite o teu e-mail')
        #add_placeholder(self.fields['first_name'], 'Ex.: John')
        #add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Digite a senha')
        add_placeholder(self.fields['password2'], 'Confirme a senha')
        add_placeholder(self.fields['estudante_interno'], 'estudante')
        add_placeholder(self.fields['numero_telefone'], 'Digite o numero de telefone')
        add_placeholder(self.fields['instituicao'], 'Digite o nome da tua instituição')
        add_placeholder(self.fields['nome_completo'], 'Digite o teu nome completo')

    username = forms.CharField(
        label='Username',
        help_text=(
            'O nome de usuário deve ter letras, números ou um desses @.+-_. '
            'O comprimento deve estar entre 4 e 150 caracteres.'
        ),
        error_messages={
            'required': 'Este campo não deve estar vazio',
            'min_length': 'O nome de usuário deve ter pelo menos 4 caracteres',
            'max_length': 'O nome de usuário deve ter menos de 150 caracteres',
        },
        min_length=4, max_length=150,
    )
    nome_completo = forms.CharField(
        error_messages={'required': 'Digite teu nome completo'},
        label='Nome Completo',
    )
    numero_telefone = forms.CharField(
        error_messages={'required': 'Digite teu número de telefone'},
        label='Número de telefone'
    )
    estudante_interno = forms.CharField(
        widget=forms.CheckboxInput(),
       # error_messages={'required': ''},
        label='É estudante interno?',
    )
    instituicao = forms.CharField(required=False,
        #error_messages={'required': 'Digite o nome da tua instituição'},
        label='Qual é a tua instituição?'
    )
    codigo_estudante = forms.IntegerField(required=False,
        error_messages={'required': 'Digite o teu código de estudante'},
        label='Código de Estudante'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail é obrigatório'},
        label='E-mail',
        help_text='O e-mail deve ser válido.',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não deve ser vazia'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        ),
        validators=[strong_password],
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirme a senha',
        error_messages={
            'required': 'Por favor, digite novamente a senha'
        },
    )
    

    class Meta:
        model = User
        fields = [
            'nome_completo',
            'numero_telefone',
            'email',
            'estudante_interno',
            'codigo_estudante',
            'instituicao',
            'username',
            
            'password',
            
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O e-mail já está em uso', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas devem ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
'''
