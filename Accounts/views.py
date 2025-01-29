from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout,login as auth_login
from django.utils.timezone import now
from datetime import timedelta
import asyncio
from asgiref.sync import sync_to_async

# Create your views here.

import uuid
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.utils.http import urlencode
from .models import Profile


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        checkbox = request.POST.get('checkbox')

        # Password validation
        if len(password) < 8:
            messages.warning(request, 'Password must be at least 8 characters long.')
            return render(request, 'Auth/registration.html', {'username': username, 'email': email, 'checkbox': checkbox})

        if password != password1:
            messages.warning(request, 'Passwords do not match.')
            return render(request, 'Auth/registration.html', {'username': username, 'email': email, 'checkbox': checkbox})


        try:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists. Please choose a different username.')
                return redirect('registration')

            if User.objects.filter(email=email).exists():
                messages.warning(request, 'An account with this email already exists. Please use a different email.')
                return redirect('registration')

            verification_token = str(uuid.uuid4())

            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            profile = Profile.objects.create(
                user=user,
                verification_token=verification_token
            )

            # Send verification email
            send_verification_email(username, email, verification_token, request)

            messages.success(request, 'A verification link has been sent to your email. Please check your inbox.')
            return redirect('login')

        except IntegrityError:
            messages.error(request, 'There was an error with your registration. Please try again.')
            return redirect('registration')

    return render(request, 'Auth/registration.html')



def send_verification_email(username, email, token, request):
    subject = 'Verify Your Account'
    verification_url = request.build_absolute_uri(reverse('verify_email') + '?' + urlencode({'token': token}))
    message = f'Hi {username},\n\nPlease click on the link below to verify your email and activate your account:\n\n{verification_url}\n\nThank you!'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def verify_email(request):
    token = request.GET.get('token')
    try:
        profile = Profile.objects.get(verification_token=token)
        profile.user.is_active = True
        profile.user.save()
        profile.is_verified = True
        profile.verification_token = None
        profile.save()

        messages.success(request, "Your account has been successfully verified.")
        return redirect('login')

    except Profile.DoesNotExist:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('login')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        print(f"Remember Me: {remember_me}")

        user = authenticate(username=username, password=password)
        print('Found User for login:', user)

        if user:
            try:
                profile = Profile.objects.get(user=user)

                if profile.is_verified:
                    auth_login(request, user)

                    if remember_me:
                        request.session.set_expiry(86400)  # 1 day
                    else:
                        request.session.set_expiry(0)

                    messages.success(request, 'You are successfully logged in!')
                    return redirect('home')

                else:
                    messages.error(request, 'Please verify your account!')
            except Profile.DoesNotExist:
                messages.error(request, 'Your profile does not exist. Please contact support.')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Auth/login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            try:
                user = User.objects.get(email=email)

                reset_token = str(uuid.uuid4())

                profile, created = Profile.objects.get_or_create(user=user)
                profile.password_reset_token = reset_token
                profile.password_reset_expires = now() + timedelta(minutes=15)
                profile.save()

                send_forget_password_mail(user.email, reset_token, request)

                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect('forgot_password')

            except User.DoesNotExist:
                messages.error(request, 'No account found with that email address.')
            except Exception as e:
                messages.error(request, 'There was an error sending the email. Please try again.')
        else:
            messages.error(request, 'Please enter a valid email address.')

    return render(request, 'Auth/forgot_password.html')



def send_forget_password_mail(email, token, request):
    subject = 'Your Forget Password Link'
    message = f' Hi, click on the link to reset your password {request.scheme}://{request.META["HTTP_HOST"]}/change_password/{token}'
    sender = settings.EMAIL_HOST_USER
    receiver = [email]
    send_mail(subject, message, sender, receiver)


def verify(request, forget_password_token):
    profile = Profile.objects.filter(reset_token=reset_token).first()
    profile.is_verified = True
    return redirect('login')



def change_password(request, token):
    try:
        # Find profile with the given reset token
        prof_obj = Profile.objects.filter(password_reset_token=token).first()

        if not prof_obj:
            messages.warning(request, "Invalid or expired token!")
            return redirect('forgot_password')

        # Check if token is expired
        if prof_obj.password_reset_expires and prof_obj.password_reset_expires < now():
            messages.warning(request, "This password reset link has expired.")
            return redirect('forgot_password')

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Check for empty fields
            if not new_password or not confirm_password:
                messages.warning(request, "Please fill out all fields!")
                return redirect(f'/change_password/{token}/')

            # Check if passwords match
            if new_password != confirm_password:
                messages.warning(request, "Passwords do not match!")
                return redirect(f'/change_password/{token}/')

            # Update password
            user = prof_obj.user
            user.set_password(new_password)
            user.save()

            # Clear the reset token
            prof_obj.password_reset_token = None
            prof_obj.password_reset_expires = None
            prof_obj.save()

            messages.success(request, "Password changed successfully! You can now log in.")
            return redirect('login')

        return render(request, 'Accounts/pass_change.html', {'user_id': prof_obj.user.id})

    except Exception as e:
        print(f"Error: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect('forgot_password')


def logout(request):
    auth_logout(request)
    messages.success(request, "User logged out!")
    return redirect('login')


