from .models import Logosettings,BusinessInfo
from Course.models import CoursePurchase,Course

def businessinfo(request):
	return {
		'businessinfo': BusinessInfo.objects.first(),
	}

def logo(request):
	return {
		'logo': Logosettings.objects.first(),
	}
