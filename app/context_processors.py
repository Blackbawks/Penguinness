from django.conf import settings
def global_settings(request):
    # return any necessary values
    return {
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_TAGLINE': settings.SITE_TAGLINE
    }
