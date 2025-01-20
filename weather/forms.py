from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя с дополнительной валидацией.

    Включает поля для ввода имени пользователя, электронной почты и пароля.
    """

    # Добавим поле электронной почты
    email = forms.EmailField(required=True, help_text="Введите действительный адрес электронной почты.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        """
        Проверка уникальности имени пользователя.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Это имя пользователя уже занято.")
        return username

    def clean_email(self):
        """
        Проверка уникальности электронной почты.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже используется.")
        return email

    def clean_password1(self):
        """
        Дополнительная валидация для пароля.
        Пароль должен содержать хотя бы одну цифру и одну заглавную букву.
        """
        password = self.cleaned_data.get('password1')

        # Проверяем, чтобы пароль был достаточно сложным
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

        return password

    def clean_password2(self):
        """
        Проверка на совпадение паролей.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return password2
