from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import RegisterForm, LoginForm, ProfileForm, CustomPasswordResetForm


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('users:profile')
        messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'profile_form': profile_form})


def signupuser(request):
    if request.user.is_authenticated:
        return redirect('quotes:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('quotes:main')
        messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = RegisterForm()

    return render(request, 'users/signup.html', {'form': form})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('quotes:main')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('quotes:main')
        messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
@require_POST
def logoutuser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('quotes:main')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class ResetPasswordView(SuccessMessageMixin, CustomPasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'