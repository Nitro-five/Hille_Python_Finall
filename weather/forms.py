from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя с дополнительной валидацией.

    Включает поля для ввода имени пользователя, электронной почты и пароля,
    а также проверку уникальности имени пользователя и адреса электронной почты.
    """

    email = forms.EmailField(required=True, help_text="Введите действительный адрес электронной почты.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с добавлением пользовательских атрибутов и текста подсказок для полей.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'custom_username_id'})
        self.fields['email'].widget.attrs.update({'id': 'custom_email_id'})
        self.fields['password1'].widget.attrs.update({'id': 'custom_password1_id'})
        self.fields['password2'].widget.attrs.update({'id': 'custom_password2_id'})

        self.fields['username'].help_text = "Имя пользователя должно быть уникальным."
        self.fields['email'].help_text = "Введите действительный адрес электронной почты."
        self.fields[
            'password1'].help_text = "Пароль должен содержать минимум 8 символов, одну цифру и одну заглавную букву."
        self.fields['password2'].help_text = "Введите тот же пароль для подтверждения."

    def clean_username(self):
        """
        Проверка уникальности имени пользователя.
        Если имя пользователя уже существует в базе данных, выбрасывается ошибка валидации.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Это имя пользователя уже занято.")
        return username

    def clean_email(self):
        """
        Проверка уникальности электронной почты.
        Если адрес электронной почты уже используется другим пользователем, выбрасывается ошибка валидации.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже используется.")
        return email

    def clean_password1(self):
        """
        Дополнительная валидация для пароля.
        Проверяется, чтобы пароль был достаточно сложным: содержал минимум 8 символов, цифры и заглавные буквы.
        """
        password = self.cleaned_data.get('password1')

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
        Если введенные пароли не совпадают, выбрасывается ошибка валидации.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return password2
