from django.shortcuts import render
from Course.models import CoursePurchase
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def userdashboard(request):
    purchased_courses = CoursePurchase.objects.filter(user=request.user, is_ordered=True).select_related('course')
    return render(request, 'Dashboard/user_dashboard.html', {
        'purchased_courses': purchased_courses,
    })