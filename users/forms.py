from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password'
        })
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'confirm password'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError(f'Passwords don`t match')

        validate_password(password)

        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError(f'Try using different username')

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.is_active = True

        if commit:
            super().save()
        return user
