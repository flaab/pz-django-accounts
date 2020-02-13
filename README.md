# Yet another Django-Accounts App

A bootstrapped and complete django accounts engine that blends into django-admin and works as desired right out of the box, without conflicting with the django-admin user experience.  It allows you to seamlessly register users into your website and it offers all the functionalities registered users need: registration, login with email or username, logout, password reset, password change, welcome dashboard, profile edition, account deactivation, account deletion, avatars, gravatars and reCaptcha protected forms.

![PZ-Django-Accounts](https://www.dropbox.com/s/5q2229bvrpsnq4q/pz-django-accounts.png?raw=1)

## What makes it different?

- It is a complete engine that works out of the box
- The templates are bootstrap-ready and fully customizable
- No conflict with the django-admin user experience

## Requirements
- Python >= 3.0
- Django >= 2.2.6
- Django-countries
- Django-resized
- Crispy-forms
- Markdown
- Hashlib

## Installation
Create a directory and clone the project.
```
$ mkdir mysite
$ cd mysite
$ git clone https://github.com/flaab/pz-django-accounts.git 
```
Create the database and tables of the application.
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
Create a superuser for django-admin.
```
$ python3 manage.py createsuperuser
```
If all went well, run the server.
```
$ python3 manage.py runserver
```
Now the server is up and running and the app is available at http://127.0.0.1:8000 and http://127.0.0.1:8000/account.

## Running the application in a existing Django Site

The above instructions will create a new Django project that will run the application. If you did that, you can skip this section. If on the other hand, you want to include the accounts application in your existing project, then another course of action is needed. Add the following lines in your *settings.py*:

```
# Imports
from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

# Installed apps
INSTALLED_APPS = (
    # ...
    'django.contrib.staticfiles',
    'account',
)

# Static files and media
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Authentication constants
LOGIN_REDIRECT_URL = reverse_lazy('account:dashboard')
LOGIN_URL = reverse_lazy('account:login')

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]

# Email backend 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = ‘smtp.server.com’
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ‘your_account@server.com’
EMAIL_HOST_PASSWORD = ‘’

# Bootstrap messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
```

Add the following lines in your *urls.py*:

```
urlpatterns = [
    # ...,
    path('account/', include(('account.urls', 'account'), namespace = 'account')),
]
if(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
```

## Customize the application
To further customize the application to do what you need, you can:

- Configure the application constants at *account/apps.py*
- Edit the **Profile** model at *account/models.py*, adding or removing user profile fields.
- Edit the **ProfileEditForm** at *account/forms.py*, adding or removing user profile fields.
- Add or edit views at *account/views.py*, adding functionality for authenticated users.
- Customize the templates at *account/templates* to look they way you want.

## Customize the templates
The templates are organized in three categories: extendable templates, includable templates and page templates. Each uses a different naming convention. The templates the application uses are the following, which you can edit to fit your needs. Stylesheets and Javascript files are hotlinked from cdn repositories but you can place your own under *account/static/*.

- *templates/_messages.html* => Template to display flash messages (error, warning, validation error, success)
- *templates/account/__l_base.html* => Base layout for the application 
- *templates/account/_recaptcha_field.html* => Template tag to display the recaptcha field
- *templates/account/_sidebar.html* => Navigation sidebar for authenticated users
- *templates/account/dashboard.html* => Page template for the welcome dashboard
- *templates/account/deactivate.html* => Page template for account deactivation
- *templates/account/delete.html* => Page template for account deletion 
- *templates/account/edit.html* => Page template for profile edition
- *templates/account/login.html* => Page template for login form
- *templates/account/password_change_done.html* => Page template for password change done
- *templates/account/password_change_form.html* => Page template for password change form
- *templates/account/password_reset_complete.html* => Page template for password reset complete
- *templates/account/password_reset_confirm.html* => Page template for password reset confirm
- *templates/account/password_reset_done.html* => Page template for password reset done
- *templates/account/password_reset_email.html* => Page template for password reset email 
- *templates/account/password_reset_failed.html* => Page template for password reset failed
- *templates/account/password_reset_form.html* => Page template for password reset form
- *templates/account/register.html* => Page template for account registration
- *templates/account/register_done.html* => Page template for account registration done

## To-do
- Welcome email with confirmation on new registrations
- Maximum log-in attempts
- 2FA Authentication

## Authors
**Arturo Lopez Perez** - Main and sole developer (so far).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details