from django.shortcuts import render

# Create your views here.
def userdashboard(request):

    return render(request, 'Dashboard/user_dashboard.html')