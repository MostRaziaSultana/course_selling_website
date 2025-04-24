from .models import Logosettings,BusinessInfo


def businessinfo(request):
	return {
		'businessinfo': BusinessInfo.objects.first(),
	}

def logo(request):
	return {
		'logo': Logosettings.objects.first(),
	}
