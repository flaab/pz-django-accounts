from django import template
from django.utils.safestring import mark_safe
from django.apps import apps

# Register
register = template.Library()

@register.simple_tag
def app_attr(name):
    """ Returns an appsettings attribute """
    return(mark_safe(getattr(apps.get_app_config('Account'), name)))

@register.inclusion_tag('account/_recaptcha_field.html')
def recaptcha_field():
    """ Prints a recaptcha field using bootstrap4 """
    recaptcha_enabled = apps.get_app_config('Account').recaptcha_enabled
    recaptcha_sitekey = apps.get_app_config('Account').recaptcha_sitekey
    return{'recaptcha_enabled': recaptcha_enabled,
           'recaptcha_sitekey': recaptcha_sitekey}