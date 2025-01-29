from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Home.views import *
from Accounts.views import *
from Userdashboard.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('verify_email/', verify_email, name='verify_email'),

    path('forgot_password/', forgot_password, name="forgot_password"),
    path('change_password/', change_password, name="change_password"),
    path('verify/', verify, name="verify"),
    path('logout/', logout, name="logout"),

    path('dashboard/', dashboard, name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
