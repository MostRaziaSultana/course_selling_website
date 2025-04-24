from django.contrib import admin
from .models import Banner,Blog,BlogCategory,BusinessInfo,Logosettings,FAQ,Brand,Achievement
# Register your models here.
admin.site.register(Banner)
admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(Logosettings)
admin.site.register(BusinessInfo)
admin.site.register(FAQ)
admin.site.register(Brand)
admin.site.register(Achievement)