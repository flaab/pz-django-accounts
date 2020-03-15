from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.views import PasswordResetView
from .decorators import login_excluded, check_recaptcha
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.apps import apps 
from .models import Profile

#------------------------------------------

@login_excluded('account:dashboard')
@check_recaptcha
def user_password_reset(request):
    
    # Check recaptcha
    if request.method == 'POST':
        if request.recaptcha_is_valid:
            return PasswordResetView.as_view(template_name = 'account/password_reset_form.html',
                                     email_template_name='account/password_reset_email.html',
                                     html_email_template_name='account/password_reset_email.html',
                                     success_url = reverse_lazy('account:password_reset_done'))(request)
        else: # Recaptcha failed
            return render(request, 'account/password_reset_failed.html', {})
    else: # No form received
        return PasswordResetView.as_view(template_name = 'account/password_reset_form.html',
                                     email_template_name='account/password_reset_email.html',
                                     html_email_template_name='account/password_reset_email.html',
                                     success_url = reverse_lazy('account:password_reset_done'))(request)

#------------------------------------------

@login_excluded(redirect_to = 'account:dashboard')
@check_recaptcha
def user_login(request):
    """ Custom login view, with authentication exclusion and recaptcha """
    
    # Form received
    if(request.method == 'POST'):
        
        # Instance of form
        form = LoginForm(request.POST)

        # If recaptacha is ok and form is valid
        if request.recaptcha_is_valid:

            # If form is valid
            if form.is_valid():
                
                # Get clean form data
                cd = form.cleaned_data
                user = authenticate(request, username = cd['username'], password = cd['password'])
                
                # User received
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('account:dashboard')
                    else: # Inactive user
                        messages.error(request, _('Your account has been disabled and is no longer active.'))
                else: # Login failed
                    messages.error(request, _('Login failed, invalid username or password. Both are case-sensitive!'))
            else: # Validation failed
                messages.error(request, _('Validation failed, please correct the errors below.'))
        else: # Recaptcha failed
            messages.error(request, _('ReCAPTCHA failed. Are you human? If so, please try again.')) 
    else:   # Form not received
        form = LoginForm()
    
    # Return
    return render(request, 'account/login.html', {
                                                'form': form, 
                                                })

#------------------------------------------

@login_excluded(redirect_to = 'account:dashboard')
@check_recaptcha
def register(request):
    """ Performs an user registration with validation and flash messages """
    
    # Proceed with form
    if request.method == 'POST':

        # Proceed
        user_form = UserRegistrationForm(request.POST)
        
        # If recaptcha ok
        if request.recaptcha_is_valid:
            # If form is valid
            if user_form.is_valid():
                new_user = user_form.save(commit=False)     # Don't save user yet
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                return render(request, 'account/register_done.html', {'user_form': user_form})
            else: # Form is not valid
                messages.error(request, _('Some errors prevented your registration, please find details below.'))
        else: # Recaptcha failed
            messages.error(request, _('ReCAPTCHA failed. Are you human? If so, please try again.')) 
    else: # No post received
        user_form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {
                                                    'user_form': user_form,
                                                    })

#------------------------------------------

@login_required
def dashboard(request):
    """ Welcomes the user if the session is active """
    return render(request, 'account/dashboard.html')

#------------------------------------------

@login_required
def edit(request):
    """ Edit the profile for logged users """

    # Form received
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user, data = request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile, data = request.POST, files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile has been successfully updated, thank you!'))
        else: 
            messages.error(request, _('Some errors prevented your profile from updating, please find details below.'))
    else: # Form not received
        user_form = UserEditForm(instance = request.user)
    
    # This is run anyway because the avatar is resized and has to be read again
    profile_form = ProfileEditForm(instance = request.user.profile)

    return render(request, 'account/edit.html', {
                                                'user_form': user_form,
                                                'profile_form': profile_form,
                                                })

#------------------------------------------

@login_required
def delete(request, confirm = 0):
    """ 
    Deletes the user account from the database and kicks him out.
    This way foreign keys are broken or cascade deletion happens 
    """
    
    # Confirm action
    if(confirm == 1):   

        # Ignore staff and superusers
        if(request.user.is_staff or request.user.is_superuser):
            messages.error(request, _('Your user profile is "superuser" or "staff" and cannot be deleted.'))
            return redirect('account:dashboard')
        else: # Logs out and tries to delete the user
            try:
                user = request.user
                logout(request)
                user.delete()
                messages.success(request, _('Your account has been successfully deleted. Goodbye!'))
            except user.DoesNotExist:
                messages.error(request, _('Your user does not exist anymore!'))
            except Exception as e:
                messages.error(request, _('Unexpected error deleting your account.'))
            
            # Exception or not, session is closed. Go to login.
            return redirect('account:login')
    
    return render(request, 'account/delete.html', {})

#------------------------------------------

@login_required
def deactivate(request, confirm = 0):
    """ 
    Deactivates the user account from the database and kicks him out.
    This way foreign keys are not broken
    """
    
    # Confirm action
    if(confirm == 1):    
        # Ignore staff and superusers
        if(request.user.is_staff or request.user.is_superuser):
            messages.error(request, _('Your user profile is "superuser" or "staff" and cannot be deactivated.'))
            return redirect('account:dashboard')
        else: # Logs out and tries to delete the user
            try:
                user = request.user
                logout(request)
                user.is_active = False
                user.save()
                messages.success(request, _('Your account has been successfully deactivated. Goodbye!'))
            except user.DoesNotExist:
                messages.error(request, _('Your user does not exist anymore!'))
            except Exception as e:
                messages.error(request, _('Unexpected error deactivating your account.'))
            
            # Exception or not, session is closed. Go to login.
            return redirect('account:login')
    
    return render(request, 'account/deactivate.html', {})