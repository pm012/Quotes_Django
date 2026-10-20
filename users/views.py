from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.db import transaction
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import (
    LoginForm,
    ProfileForm,
    RegisterForm,
    UserAdministrationForm,
    UserNameForm,
)


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_staff)(view_func)


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserNameForm(request.POST, instance=request.user)
        profile_is_valid = profile_form.is_valid()
        user_is_valid = user_form.is_valid()
        if profile_is_valid and user_is_valid:
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('users:profile')
        messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserNameForm(instance=request.user)

    return render(request, 'users/profile.html', {
        'profile_form': profile_form,
        'user_form': user_form,
    })


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


class ResetPasswordView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    subject_template_name = 'users/password_reset_subject.txt'


@staff_required
def user_administration(request):
    users = User.objects.order_by('username')
    return render(request, 'users/user_administration.html', {'users': users})


@staff_required
def edit_user(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot edit your own account here.")
        return redirect('users:user_administration')

    if request.method == 'POST':
        form = UserAdministrationForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account '{target_user.username}' was updated.")
            return redirect('users:user_administration')
    else:
        form = UserAdministrationForm(instance=target_user)

    return render(request, 'users/edit_user.html', {
        'form': form,
        'target_user': target_user,
    })


@staff_required
@require_POST
def delete_user(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot delete your own account.")
    else:
        username = target_user.username
        target_user.delete()
        messages.success(request, f"Account '{username}' was deleted.")
    return redirect('users:user_administration')