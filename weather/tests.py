from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationFormTests(TestCase):
    """
    Тесты для проверки формы регистрации пользователей.
    """

    def setUp(self):
        """
        Настраивает URL для регистрации перед запуском тестов.
        """
        self.register_url = reverse('register')

    def test_registration_page_status_code(self):
        """
        Проверяет, что страница регистрации доступна (возвращает статус-код 200).
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_registration_form_submission_valid(self):
        """
        Проверяет успешную регистрацию пользователя при корректных данных.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Ожидается перенаправление
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_form_submission_invalid(self):
        """
        Проверяет отклонение регистрации при несовпадении паролей.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'WeakPassword456!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)  # Проверяем, что форма передана в контекст
        self.assertTrue(form.errors)  # Убедимся, что есть ошибки
        self.assertIn('password2', form.errors)  # Ошибка в поле "password2"
        self.assertIn('Пароли не совпадают.', form.errors['password2'])

    def test_registration_form_missing_email(self):
        """
        Проверяет отклонение регистрации при отсутствии email.
        """
        data = {
            'username': 'testuser',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)  # Проверяем, что форма передана в контекст
        self.assertTrue(form.errors)  # Убедимся, что есть ошибки
        self.assertIn('email', form.errors)  # Ошибка в поле "email"
        self.assertEqual(form.errors['email'], ['This field is required.'])
