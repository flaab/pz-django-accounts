from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.apps import apps
import hashlib 

class Profile(models.Model):
    """ User profile for users, displayed inline in admin site """
    user    = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = _("user"))
    address = models.CharField(blank = True, null = True, max_length=255, verbose_name = _("address"))
    city    = models.CharField(blank = True, null = True, max_length=255, verbose_name = _("city"))
    zipcode = models.CharField(blank = True, null = True, max_length=32, verbose_name = _("zip Code"))
    country_of_residence = CountryField(blank = True, null = True, verbose_name = _('country of residence'))
    website = models.URLField(blank = True, null = True, verbose_name = _("website"))
    date_of_birth = models.DateField(blank = True, null = True, verbose_name = _("date of birth"))
    avatar = ResizedImageField(
                size=[apps.get_app_config('Account').avatar_width, apps.get_app_config('Account').avatar_height], 
                crop=['middle', 'center'], 
                upload_to = 'users/%Y/%m/%d/', 
                force_format = 'PNG',
                blank = True, null = True, 
                quality = 90,
                verbose_name = _("Avatar"))


    def get_avatar(self):
        """ Returns the avatar for this user or the gravatar url """
        if not self.avatar:
            return(self.gravatar_url())
        else:
            l_avatar = self.avatar
            return(settings.MEDIA_URL + str(l_avatar))


    def gravatar_url(self):
        """ Gets the URL for the gravatar for this user, used if no native avatar """
        md5 = hashlib.md5(self.user.email.encode())
        digest = md5.hexdigest()
        return('http://www.gravatar.com/avatar/{}'.format(digest))


    def get_first_name(self):
        """ Gets the first name, if present. Else return username. """
        if self.user.first_name:
            return(self.user.first_name)
        else:
            return(self.user.username)


    def get_full_name(self): 
        """ Returns a string representation of this user """
        """ If no first and last name is provided, username is displayed """
        if(self.user.first_name and self.user.last_name):
            return(self.user.first_name +" "+ self.user.last_name)
        else:
            return self.user.username


    def __str__(self): 
        """ Returns a string representation of this user """
        return(self.get_full_name())


    def save(self, *args, **kwargs):
        """ Clean old avatar file before uploading new one """
        try:
            this = Profile.objects.get(id = self.id)
            if this.avatar != self.avatar:
                this.avatar.delete()
        except: pass
        super(Profile, self).save(*args, **kwargs)

# Signal to sync profile to user on sql transactions
@receiver(post_save, sender = User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
    instance.profile.save()

# Signal to delete media on profile deletion
@receiver(post_delete, sender = Profile)
def delete_user_profile(sender, instance, **kwargs):
    """ Deletes media objects on deletion of this model """
    instance.avatar.delete(False)  