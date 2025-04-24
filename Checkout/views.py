# from django.shortcuts import render,redirect
# from.models import CustomUser
# import random
# from django.conf import settings
# from django.core.mail import send_mail
# from django.contrib import messages
# from django.db import IntegrityError
# from django.contrib.auth import authenticate, login, logout,login as auth_login
# from django.contrib.auth import logout as auth_logout
#
# # Create your views here.
#
# def registration(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password1 = request.POST.get('password1')
#         checkbox = request.POST.get('checkbox')
#         print(f'username: {username}, email: {email}, password: {password}, '
#               f'password1: {password1}, checkbox: {checkbox}')
#
#         # Validate password length
#         if len(password) < 8:
#             messages.warning(request, 'Password must be at least 8 characters long.')
#             return render(request, 'Auth/registration.html', {
#                 'username': username,
#                 'email': email,
#                 'checkbox': checkbox
#             })
#
#
#         if password != password1:
#             messages.warning(request, 'Passwords do not match.')
#             return render(request, 'Auth/registration.html', {
#                 'username': username,
#                 'email': email,
#                 'checkbox': checkbox
#             })
#
#         if checkbox != 'on':
#             messages.warning(request, 'You must agree to the terms and policy.')
#             return render(request, 'Auth/registration.html', {
#                 'username': username,
#                 'email': email
#             })
#
#         try:
#             if CustomUser.objects.filter(username=username).exists():
#                 messages.warning(request, 'Username already exists. Please choose a different username.')
#                 return redirect('registration')
#
#             if CustomUser.objects.filter(email=email).exists():
#                 messages.warning(request, 'An account with this email already exists. Please use a different email.')
#                 return redirect('registration')
#
#
#             otp = random.randint(1000, 9999)
#             user = CustomUser.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password,
#                 otp=otp,
#             )
#             user.save()
#
#             # Call the function to send OTP email
#             send_otp_email(username, email, otp)
#             messages.success(request, 'Please check your mail for an OTP.')
#             return redirect('registration')
#
#         except IntegrityError as e:
#             messages.error(request, 'There was an error with your registration. Please try again.')
#             return redirect('registration')
#
#     return render(request, 'Auth/registration.html')
#
#
# def send_otp_email(username, email, otp):
#     subject = 'Your Account Verification OTP'
#     message = f'Hi {username}, thank you for registering. Here is your OTP: {otp}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)
#
#
# def otp_verify(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         print('Received OTP:', otp)
#
#         if otp:
#             user = CustomUser.objects.filter(otp = otp).first()
#             print('Found User:', user)
#
#             if user:
#                 user.is_verified = True
#                 user.save()
#                 messages.success(request, 'Account Verified, Please log in!')
#                 return redirect('login')
#             else:
#                 messages.error(request, 'Invalid OTP!')
#             return redirect('registration')
#
#     return redirect('registration')
#
#
# def login(request):
#
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         remember_me = request.POST.get('remember_me')
#         print(f"Remember Me: {remember_me}")
#
#         user = authenticate(username=username, password=password)
#         print('Found User for login:', user)
#         if user:
#             if user.is_verified:
#                 auth_login(request, user)
#
#                 if remember_me:
#                     request.session.set_expiry(86400)  # 1 day
#                 else:
#                     request.session.set_expiry(0)
#
#                 messages.success(request, 'You are successfully logged in! ')
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Please verify the account! ')
#         else:
#             messages.error(request, 'Invalid username or password.')
#
#     return render(request, 'Auth/login.html')
#
#
# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#
#         if email:
#             try:
#                 # Find user by email
#                 user = CustomUser.objects.get(email=email)
#
#                 # Generate OTP
#                 otp = random.randint(1000, 9999)
#                 user.otp = otp
#                 user.save()
#
#                 # Send email with OTP
#                 subject = 'Your Account Reset OTP'
#                 message = f'Hi {user.username}, here is your OTP: {otp}'
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [email]
#
#                 send_mail(subject, message, email_from, recipient_list)
#
#                 messages.success(request, 'OTP has been sent to your email address.')
#             except CustomUser.DoesNotExist:
#                 messages.error(request, 'No account found with that email address.')
#             except Exception as e:
#                 messages.error(request, 'There was an error sending the OTP. Please try again.')
#         else:
#             messages.error(request, 'Please enter a valid email address.')
#
#     return render(request, 'Auth/forgot_password.html')
#
#
# def submit_otp(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         newpass = request.POST.get('new_password')
#
#         if otp:
#             user = CustomUser.objects.filter(otp=otp).first()
#             print('Found User:', user)
#
#             if user:
#                 user.password = newpass
#                 user.set_password = newpass
#                 user.save()
#                 messages.success(request, 'Password reset successfully! You can now log in with your new password.')
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Invalid OTP!')
#             return redirect('forgot_password')
#
#     return redirect('user_auth')
#
#
# def logout(request):
#     auth_logout(request)
#     messages.success(request, "User logged out!")
#     return redirect('login')
#
#
