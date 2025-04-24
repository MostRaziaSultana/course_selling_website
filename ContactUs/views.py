from django.shortcuts import render
from .models import UserMessage,ContactUs
from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.
def contact(request):
    contact = ContactUs.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(f"Saving message: {name}, {email}, {subject}, {message}")

        try:
            UserMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, 'Message sent successfully!')
            return redirect(request.META.get('HTTP_REFERER'))

        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'There was an error sending your message. Please try again later.')
            return redirect(request.META.get('HTTP_REFERER'))

    return render(request,'contact/contact.html' ,{'contact': contact, })

