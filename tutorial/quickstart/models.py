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
    email=models.EmailField(max_length=200,help_text='Required')
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    password=models.CharField(max_length=100,default=None,null=True)
    confirm_password=models.CharField(max_length=100,default=None,null=True)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{10,10}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(max_length=10,blank=False)
    
    
     
    class Meta:
        verbose_name =('User')
        verbose_name_plural = ('Users')
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

    class Meta:
        verbose_name=('OTP')
        verbose_name_plural=('OTPs')

    def __str__(self):
        return ("%s has received otps: %s" %(self.receiver.username,self.otp))


class Friend(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='friends_list')
    friends=models.ManyToManyField(User)

    def __str__(self):
        return "Friend List of %s"%(self.user.username)




class GroupModel(models.Model):

    name=models.CharField(max_length=200)
    users=models.ManyToManyField(User,related_name='group_members')
    type_choices=[
        ('APARTMENT','Apartment'),
        ('HOUSE','House'),
        ('TRIP','Trip'),
        ('OTHER','Other'),
    ]
    type=models.CharField(max_length=200,choices=type_choices,default="Trip")
    # created_by=models.ForeignKey(User,default=None,on_delete=models.CASCADE,related_name="admin")
    created_at=models.DateTimeField(auto_now_add=True)
    admin=models.ForeignKey(User,default=None,on_delete=models.CASCADE,related_name='admin')
    class Meta:
        verbose_name=('Group')
        verbose_name_plural=('Groups')

    # def __str__(self):
    #     return self.name
    
class Expense(models.Model):

    bill_name=models.CharField(max_length=200)
    description=models.TextField(default=None)
    group_name=models.ForeignKey(GroupModel,default=None,on_delete=models.CASCADE)
    amount=models.DecimalField(default=0,max_digits=10,decimal_places=4)
    payer=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s in : %s "%(self.bill_name,self.group_name.name)



class Status(models.Model):
    ower=models.ForeignKey(User,default=None,on_delete=models.CASCADE,related_name='Ower')
    lender=models.ForeignKey(User,default=None,on_delete=models.CASCADE,related_name='Lender')
    amount=models.DecimalField(default=None,max_digits=10,decimal_places=4)
    
    class Meta:
        verbose_name=("Status")
        verbose_name_plural=("Status")

    def __str__(self):
        return "%s has lended %s to %s" %(self.ower,self.lender,self.amount)   

    

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