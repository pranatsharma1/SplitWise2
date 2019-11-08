from django.contrib import admin
from .models import User,OTP,GroupModel

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
        ("Group Members",{"fields":["users,"] }),
        ("Type Of Gr")
    ]

admin.site.register(User,UserAdmin)
admin.site.register(OTP)
admin.site.register(GroupModel)