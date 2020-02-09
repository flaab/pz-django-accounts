from django import forms
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from .models import Profile
from .widgets import PreviewImageWidget

#------------------------------------------

class LoginForm(forms.Form):
    """ Login form for users """
    username = forms.CharField(label = "Username or Email Address")
    password = forms.CharField(widget = forms.PasswordInput)

#------------------------------------------

class UserRegistrationForm(forms.ModelForm):
    """ Registration form for new users """
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)
    first_name = forms.CharField(label = 'First name', required = True)
    last_name = forms.CharField(label = 'Last name', required = True)
    email = forms.EmailField(label = 'Email address', required = True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

    def clean_password2(self):
        cd = self.cleaned_data 
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match, please try again')
        return cd['password2']

#------------------------------------------

class UserEditForm(forms.ModelForm):
    """ Edit user forms """
    first_name = forms.CharField(label = 'First name', required = True)
    last_name = forms.CharField(label = 'Last name', required = True)
    email = forms.EmailField(label = 'Email address', required = True)

    class Meta:
        model = User
        fields = ('first_name','last_name','email')       

#------------------------------------------

class ProfileEditForm(forms.ModelForm):
    """ Change user profile form """
    date_of_birth = forms.DateField(help_text = "Enter a valid date in YYYY-mm-dd format", required = False)
    avatar = forms.ImageField(required = False, widget = PreviewImageWidget)

    class Meta:
        model = Profile
        fields = ('website','address','city','zipcode','country_of_residence','date_of_birth','avatar')