from django.contrib import admin
from .models import UserProfile,accountToken
# Register your models here.
class UserProfile_admin(admin.ModelAdmin):
    list_display = ['id','fullName','phoneNumber']
    class Meta:
        model=UserProfile
admin.site.register(UserProfile,UserProfile_admin)



class accountToken_admin(admin.ModelAdmin):
    # list_display = ['__str__','full_name','phoneNumber']
    class Meta:
        model=accountToken
admin.site.register(accountToken)


