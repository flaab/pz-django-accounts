from django.contrib.auth.models import User 

class EmailAuthBackend(object):
    """ Authenticates users using email address """

    def authenticate(self, request, username = None, password = None):
        """ Authenticates an user using an email, received in the username parameter """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return(user)
            else:
                return None 
        except User.DoesNotExist:
            return None 

    def get_user(self, user_id):
        """ Returns the user object for this authentication class """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
