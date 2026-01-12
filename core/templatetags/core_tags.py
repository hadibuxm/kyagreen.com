from django import template
from core.models import ContactInfo

register = template.Library()


@register.simple_tag
def get_contact_info():
    """Get contact information for use in templates"""
    return ContactInfo.load()
