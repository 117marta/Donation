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


class RemindPasswordForm(forms.Form):
    email = forms.EmailField(label='Podaj swój adres e-mail:', widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='Podaj nowe hasło:',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}),
    )
    new_password2 = forms.CharField(
        label='Potwierdź nowe hasło:',
        widget=forms.PasswordInput(attrs={'placeholder': 'Potwierdź hasło'}),
    )

    def clean(self):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise ValidationError for any errors.
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password2 = cleaned_data.get('new_password2')

        if new_password != new_password2:
            raise forms.ValidationError('Hasła różnią się od siebie!')
