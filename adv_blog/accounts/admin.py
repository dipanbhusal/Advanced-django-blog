from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel 
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = UserModel
    list_display = ( 'email','username','first_name','last_name','created_at')
    search_fields = ('email',)

admin.site.register(UserModel,CustomUserAdmin)
 