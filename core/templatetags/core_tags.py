from django import template
from core.models import ContactInfo

register = template.Library()


@register.simple_tag
def get_contact_info():
    """Get contact information for use in templates"""
    return ContactInfo.load()


@register.inclusion_tag('products/category_tree.html')
def render_category_tree(categories, selected_category=None):
    """Recursively render category tree with all nested levels"""
    return {
        'categories': categories,
        'selected_category': selected_category,
    }
