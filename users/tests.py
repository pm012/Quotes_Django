import pytest
from django.urls import reverse
from django.contrib.auth.models import User


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

    def test_register_invalid_data(client):
        # Sending invalid sign up data 
        response = client.post(reverse('users:signup'), data={'username': '', 'password': '123'})
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_login_invalid_credentials(client):
        # Incorrect password
        response = client.post(reverse('users:login'), data={'username': 'wronguser', 'password': 'wrongpassword'})
        assert response.status_code == 200
        assert response.context['form'].errors

    def test_user_profile_str(user):
        # Testing of __str__ profile method
        assert str(user.profile) == user.username