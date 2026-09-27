import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUsersViews:
    def test_signup_view(self, client):
        response = client.get(reverse('users:signup'))
        assert response.status_code == 200

    def test_profile_signal_creates_profile(self):
        user = User.objects.create_user(username='signaluser', password='password123')
        assert hasattr(user, 'profile')
        # Consider upper-case letter "P" у __str__ of the Profile model
        assert str(user.profile) == "signaluser's Profile"

    def test_login_logout_views(self, client):
        user = User.objects.create_user(username='loginuser', password='password123')
        
        login_res = client.post(reverse('users:login'), {
            'username': 'loginuser',
            'password': 'password123'
        })
        assert login_res.status_code == 302

        profile_res = client.get(reverse('users:profile'))
        assert profile_res.status_code == 200

        logout_res = client.post(reverse('users:logout'))
        assert logout_res.status_code == 302

    def test_register_invalid_data(self, client):
        response = client.post(reverse('users:signup'), data={'username': '', 'password': '123'})
        assert response.status_code == 200

    def test_login_invalid_credentials(self, client):
        response = client.post(reverse('users:login'), data={'username': 'wronguser', 'password': 'wrongpassword'})
        assert response.status_code == 200

    

    def test_user_profile_str(self):
        user = User.objects.create_user(username='testprofileuser', password='password123')
        # Awaiting row with added "'s Profile"
        assert str(user.profile) == f"{user.username}'s Profile"

    def test_profile_view_authenticated(self, client, db):
        user = User.objects.create_user(username='profileuser', password='password123')
        client.force_login(user)
        response = client.get(reverse('users:profile'))
        assert response.status_code == 200

    def test_password_reset_views(self, client):
        # Verification of availability of reset password pages
        response = client.get(reverse('users:password_reset'))
        assert response.status_code == 200

        post_resp = client.post(reverse('users:password_reset'), {'email': 'test@example.com'})
        assert post_resp.status_code in (200, 302)

    def test_profile_model_methods(self, db):
        user = User.objects.create_user(username='avataruser', password='password123')
        # Check save() profile method, if there is handling of photo/avatar
        user.profile.save()
        assert user.profile.user == user

    def test_user_form_validation(self):
        from users.forms import RegisterForm  # or ProfileForm / ResetPasswordForm
        # Тестуємо невалідний кастомний кейс (наприклад, невірно вказаний email/пароль)
        form = RegisterForm(data={'username': 'usr', 'email': 'invalid-email', 'password1': '123', 'password2': '321'})
        assert not form.is_valid()