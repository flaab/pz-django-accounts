from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class AccountConfig(AppConfig):

    # Short name for the application, used to get attributes
    label = 'Account'                                        

    # Name for the application to be included in INSTALLED_APPS
    name = 'account'                                        

    # App name for the Administration Site
    verbose_name  = "Django Accounts"
    
    # Application settings 
    meta_title         = _("My Site")                               # Meta Title
    header_title       = "Django<strong>Accounts</strong>"          # Header Title
    header_description = _("A reusable accounts app for Django")    # Header Description
    footer             = _("Proudly powered by PZ-Django-Accounts") # Footer message

    # Avatar image sizes
    avatar_width  = 300
    avatar_height = 300

    # Recaptcha
    recaptcha_enabled = True
    recaptcha_sitekey = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI' 
    recaptcha_secret  = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
