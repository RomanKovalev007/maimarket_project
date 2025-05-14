from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин или Почта", widget=forms.TextInput(attrs={'placeholder': 'Введите email',
                                                          'class': "form__box-input",
                                                           'pattern': "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                                                          'title': "Введите корректный email, например: example@mail.com"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль',
                                                                 'class': "form__box-input",
                                                                 'minlength':"8",
                                                                 "pattern":"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$" }))
class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Придумайте логин', 'class': "form__box-input",
                                                           'pattern': "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль', 'class': "form__box-input",
                                                                 'minlength':"8",
                                                                 "pattern":"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"}))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль', 'class': "form__box-input",
                                                                 'minlength':"8",
                                                                 "pattern":"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Введите вашу почту', 'class': "form__box-input",
                                                           'pattern': "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"}))

    class Meta:
        model = get_user_model()

        fields = ['username', 'password1', 'password2', 'email']

        def clean_email(self):
            email = self.cleaned_data['email']
            if get_user_model().objects.filter(email=email).exists():
                raise ValidationError('Пользователь с таким email уже существует')
