from django.contrib import admin
from .models import CourseCategory,Course,Coupon,CoursePurchase,SiteSettings
# Register your models here.
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Coupon)
admin.site.register(CoursePurchase)
admin.site.register(SiteSettings)
