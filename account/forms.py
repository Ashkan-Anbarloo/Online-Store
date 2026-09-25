from django import forms 
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import ShopUser , Address
from django.contrib.auth.forms import AuthenticationForm



class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone','first_name','last_name','is_active','is_staff','is_superuser','date_joined')
        #,'first_name','last_name','address','is_active','is_staff','is_superuser','date_joined'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('phone already exists .')
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('phone already exists .')
        if not phone.isdigit():
            raise forms.ValidationError('phone must be number .')
        if not phone.startswith('09'):
            raise forms.ValidationError('phone must start with 09 digit .')
        if len(phone) != 11:
            raise forms.ValidationError('phone must have 11 digits .')
        return phone


class ShopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ('phone','first_name','last_name','is_active','is_staff','is_superuser','date_joined')
    
    def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if self.instance.pk:
                if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('phone already exists .')
            else:
                if ShopUser.objects.filter(phone=phone).exists():
                    raise forms.ValidationError('phone already exists .')
            if not phone.isdigit():
                raise forms.ValidationError('phone must be number .')
            if not phone.startswith('09'):
                raise forms.ValidationError('phone must start with 09 digit .')
            if len(phone) != 11:
                raise forms.ValidationError('phone must have 11 digits .')
            return phone



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Phone' , max_length=11 , required=True)
    password = forms.CharField(max_length=250 , required=True , widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20 , widget=forms.PasswordInput , label='password')
    password2 = forms.CharField(max_length=20 , widget=forms.PasswordInput , label='password')

    class Meta:
        model = ShopUser
        fields = ['phone' , 'first_name' , 'last_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسورد ها مطابقت ندارند !')
        return cd['password2']
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('phone already exists!')
        return phone



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'alley', 'plaque']



class UserEditForm(forms.ModelForm):
    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name']



    