from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.contrib.auth.password_validation import validate_password
from django.core import validators


# Create your models here.
class User(AbstractUser):
    username=models.CharField(max_length=200,unique=True)
    email=models.EmailField(max_length=200,unique=True,help_text='Required')
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

     
class Meta:
    verbose_name =('user')
    verbose_name_plural = ('users')
    # abstract=True

    def __str__(self):
        return self.username



class OTP(models.Model):
    """
    Model to store Otp of user And verify user.
    """
    receiver = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField(null=False,blank=False)
    sent_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ("%s has received otps: %s" %(self.receiver.username,self.otp))












# from django import forms
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext as _
# import re

# def PasswordValidator(password):
#         if re.search('[A-Z]', password)==None and re.search('[0-9]', password)==None and re.search('[^A-Za-z0-9]', password)==None:
#             raise ValidationError(
#                 _("This password is not strong."),
#                 code='password_is_weak',
#             )

# def get_help_text(self):
#         return _("Your password must contain at least 1 number, 1 uppercase and 1 non-alphanumeric character.")


 # password = forms.CharField(max_length=32, widget=forms.PasswordInput, validators=[PasswordValidator])



    # phone_number=PhoneNumberField(null=False,blank=False,unique=True,default="")
    # password=models.CharField(max_length=200)