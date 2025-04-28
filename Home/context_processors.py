from .models import Logosettings,BusinessInfo,Blog
from Course.models import CoursePurchase,Course
from ContactUs.models import UserMessage

def businessinfo(request):
	return {
		'businessinfo': BusinessInfo.objects.first(),
	}

def logo(request):
	return {
		'logo': Logosettings.objects.first(),
	}
def homepage(request):
    latest_course_purchases = CoursePurchase.objects.select_related('user', 'course').order_by('-purchase_date')[:10]
    total_courses_count = Course.objects.count()
    total_messages_count = UserMessage.objects.count()
    total_course_purchases_count = CoursePurchase.objects.count()
    total_blog_count = Blog.objects.count()

    return {
        'latest_course_purchases': latest_course_purchases,
        'total_courses': total_courses_count,
        'total_messages': total_messages_count,
        'total_course_purchases': total_course_purchases_count,
        'total_blogs': total_blog_count,
    }