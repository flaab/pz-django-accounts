from django import forms
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .widgets import PreviewImageWidget
from .models import Profile

#------------------------------------------

class LoginForm(forms.Form):
    """ Login form for users """
    username = forms.CharField(label = _("Username or Email Address"))
    password = forms.CharField(widget = forms.PasswordInput, label = _('Password'))

#------------------------------------------

class UserRegistrationForm(forms.ModelForm):
    """ Registration form for new users """
    password = forms.CharField(label = _('Password'), widget = forms.PasswordInput)
    password2 = forms.CharField(label = _('Confirm password'), widget = forms.PasswordInput)
    first_name = forms.CharField(label = _('First name'), required = True)
    last_name = forms.CharField(label = _('Last name'), required = True)
    email = forms.EmailField(label = _('Email address'), required = True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

    def clean_password2(self):
        cd = self.cleaned_data 
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Passwords do not match, please try again'))
        return cd['password2']

#------------------------------------------

class UserEditForm(forms.ModelForm):
    """ Edit user forms """
    first_name = forms.CharField(label = _('First name'), required = True)
    last_name = forms.CharField(label = _('Last name'), required = True)
    email = forms.EmailField(label = _('Email address'), required = True)

    class Meta:
        model = User
        fields = ('first_name','last_name','email')       

#------------------------------------------

class ProfileEditForm(forms.ModelForm):
    """ Change user profile form """
    date_of_birth = forms.DateField(help_text = _("Enter a valid date in YYYY-mm-dd format"), 
                                    required = False, 
                                    label = _("Date of birth"))
    avatar = forms.ImageField(required = False, widget = PreviewImageWidget, label = _("Avatar"))

    class Meta:
        model = Profile
        fields = ('website','address','city','zipcode','country_of_residence','date_of_birth','avatar')