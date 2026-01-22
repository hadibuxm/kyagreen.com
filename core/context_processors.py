from .models import ContactInfo, SiteSettings


def contact_info(request):
    """Make contact info available to all templates"""
    return {
        'contact_info': ContactInfo.load(),
        'site_settings': SiteSettings.load()
    }
