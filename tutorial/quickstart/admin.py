from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets= [
        ("Username", {"fields": ["username",] }),
        ("Name",{"fields":["first_name","last_name",]}),
        ("Email",{"fields":["email"] }),
        ("Phone Number", {"fields": ["phone_number"]}),
        ("Password",{"fields":["password"]}),
    ]

class GroupAdmin(admin.ModelAdmin):
    fieldsets=[
        ("Group Name",{"fields":["name",] }),
        ("Group Members",{"fields":["users",] }),
        ("Type Of Group",{"fields":["type",] }),
    ]
class OTPAdmin(admin.ModelAdmin):
    fieldsets=[
        ("OTP",{"fields":["otp",] })
    ]
admin.site.register(User,UserAdmin)
admin.site.register(OTP,OTPAdmin)
admin.site.register(GroupModel,GroupAdmin)
admin.site.register(Expense)