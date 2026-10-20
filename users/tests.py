import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings

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
        assert b'id="avatar-preview"' in response.content
        assert b'id_first_name' in response.content
        assert b'id_last_name' in response.content
        assert b'users/profile.js' in response.content

    def test_profile_updates_first_and_last_name(self, client, db):
        user = User.objects.create_user(username='profileuser', password='password123')
        client.force_login(user)

        response = client.post(reverse('users:profile'), {
            'first_name': 'Ada',
            'last_name': 'Lovelace',
        })

        assert response.status_code == 302
        user.refresh_from_db()
        assert user.first_name == 'Ada'
        assert user.last_name == 'Lovelace'

    def test_password_reset_views(self, client):
        # Verification of availability of reset password pages
        response = client.get(reverse('users:password_reset'))
        assert response.status_code == 200

        post_resp = client.post(reverse('users:password_reset'), {'email': 'test@example.com'})
        assert post_resp.status_code in (200, 302)

    @override_settings(MAILERS={
        'default': {
            'BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
        },
    }, DEFAULT_FROM_EMAIL='reset@example.com')
    def test_password_reset_does_not_reveal_unknown_email(self, client):
        User.objects.create_user(
            username='reset-user',
            email='known@example.com',
            password='valid-password-123',
        )

        unknown_response = client.post(
            reverse('users:password_reset'),
            {'email': 'unknown@example.com'},
            follow=True,
        )
        known_response = client.post(
            reverse('users:password_reset'),
            {'email': 'known@example.com'},
            follow=True,
        )

        assert unknown_response.status_code == known_response.status_code == 200
        assert unknown_response.content == known_response.content
        assert len(mail.outbox) == 1
        assert mail.outbox[0].from_email == 'reset@example.com'

    @pytest.mark.django_db
    def test_user_administration_permissions_and_self_protection(self, client):
        admin = User.objects.create_user(
            username='site-admin',
            password='admin-password-123',
            is_staff=True,
        )
        other_user = User.objects.create_user(
            username='managed-user',
            password='user-password-123',
        )

        page_url = reverse('users:user_administration')
        edit_url = reverse('users:edit_user', args=[other_user.pk])
        delete_url = reverse('users:delete_user', args=[other_user.pk])
        assert client.get(page_url).status_code == 302

        client.force_login(admin)
        page = client.get(page_url)
        assert page.status_code == 200
        assert b'Current account' in page.content
        assert client.get(reverse('users:edit_user', args=[admin.pk])).status_code == 302

        response = client.post(edit_url, {
            'username': 'managed-user',
            'email': '',
            'first_name': 'Managed',
            'last_name': 'Person',
            'is_active': 'on',
            'is_staff': 'on',
        })
        assert response.status_code == 302
        other_user.refresh_from_db()
        assert other_user.first_name == 'Managed'
        assert other_user.is_staff

        assert client.post(reverse('users:delete_user', args=[admin.pk])).status_code == 302
        admin.refresh_from_db()
        assert User.objects.filter(pk=admin.pk).exists()
        assert client.post(delete_url).status_code == 302
        assert not User.objects.filter(pk=other_user.pk).exists()

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