from django.contrib import admin
from .models import ShopUser , Address
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm , ShopUserCreationForm
# Register your models here.

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


@admin.register(ShopUser)
class UserAdmin(UserAdmin):
    model = ShopUser
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    ordering = ['phone']
    list_display = ['phone' , 'first_name' , 'last_name' , 'is_staff' , 'is_active' , 'email']
    inlines = [AddressInline]
    # readonly_fields = ('last_login' , 'date_joined')

    fieldsets = (
        (None , {'fields':('phone','password')}),
        ('personal info',{'fields':('first_name' , 'last_name' ,)}),
        ('permissions',{'fields':('is_active' , 'is_staff' , 'is_superuser' , 'groups' , 'user_permissions')}), # 
        ('Important dates' , {'fields':('last_login' , 'date_joined')}),
    )
    add_fieldsets = (
        # (None, {
        #     'classes': ('wide',),
        #     'fields': ('phone', 'first_name', 'last_name', 'address', 'password1', 'password2', 'is_active', 'is_staff'),
        # }),
        (None , {'fields':('phone','password1','password2')}),
        ('personal info',{'fields':('first_name' , 'last_name' ,)}),
        ('permissions',{'fields':('is_active' , 'is_staff' , 'is_superuser' , 'groups' , 'user_permissions')}),
        ('Important dates' , {'fields':('last_login' , 'date_joined',)}),
    )


    

