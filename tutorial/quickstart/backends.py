from django.contrib.auth import get_user_model
User = get_user_model()


def EmailOrUsername(self,uname_or_em,password):
    """
    function to login the user either by email or username.
    :param self:
    :param uname_or_em:
    :param password:
    :return:
    """
    for user in User.objects.all():
        if user.email == uname_or_em and user.is_active == True:
            email = uname_or_em
            username=None
            break
        elif user.username == uname_or_em and user.is_active == True:
            username = uname_or_em
            email = None
            break
        else:
            username = None
            email = None

    if username is None and email is None:
        return 2     #no such user

    if email is not None:
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user  #Valid user
            else:
                return 3  #password incorrect
        except User.DoesNotExist:
            return 3 #Password incorrect
    if username is not None:
        try:
            user = User.objects.get(username =username)
            if user.check_password(password):
                return user
            else:
                return 3 #incorrect password
        except User.DoesNotExist:
            return 3 #Password Incorrect
