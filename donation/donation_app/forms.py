from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Wymagane',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Wpisz hasło'}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}),
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        }
