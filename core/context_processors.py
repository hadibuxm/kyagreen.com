from .models import ContactInfo


def contact_info(request):
    """Make contact info available to all templates"""
    return {
        'contact_info': ContactInfo.load()
    }
