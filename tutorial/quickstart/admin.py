from django.contrib import admin
from .models import User,OTP

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets= [
        ("Username", {"fields": ["username",] }),
        ("Name",{"fields":["first_name","last_name",]}),
        ("Email",{"fields":["email"] }),
        ("Phone Number", {"fields": ["phone_number"]}),
        ("Password",{"fields":["password"]}),
    ]
    
admin.site.register(User,UserAdmin)
admin.site.register(OTP)