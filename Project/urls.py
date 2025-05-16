from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Home.views import *
from Accounts.views import *
from Course.views import *
from Userdashboard.views import *
from ContactUs.views import *
from authority import urls as authority_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include(authority_urls)),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('change_password/<token>/', change_password, name="change_password"),
    path('logout/', logout, name="logout"),

    path('userdashboard/', userdashboard, name="userdashboard"),
    path('dashboard/course/<int:course_id>/', dashboard_course_details, name='dashboard_course_details'),

    path('contact/', contact, name="contact"),

    path('blogs/', blogs, name="blogs"),
    path('blog/<int:id>/', blog_details, name='blog_details'),

    path('faq/', faq, name="faq"),
    path('verify-email/', verify_email, name="verify_email"),

    path('all_courses/', all_courses, name="all_courses"),
    path('course/<int:id>/', course_details, name='course_details'),
    path('checkout/<int:id>/', checkout, name='checkout'),

    path('sslcommerz/', sslcommerz, name='sslcommerz'),
    path('Course/success/', success, name='success'),
    path('Course/fail/', fail, name='fail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
