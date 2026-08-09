from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from django.utils import timezone
# Create your models here.

class ShopUserManager(BaseUserManager):
    def create_user(self , phone , password=None , **extra_fields):
        if not phone:
            raise ValueError('you must provide a phone')
        user = self.model(phone=phone , **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self , phone=None , password=None , **extra_fields):
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True')

        return self.create_user(phone , password , **extra_fields)
    

class ShopUser(AbstractBaseUser , PermissionsMixin):
    phone = models.CharField(max_length=11 , unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    # address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    
    objects = ShopUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} - {self.last_name} : {self.phone}'
    

class Address(models.Model):
    user = models.ForeignKey(ShopUser , related_name='address' , on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    alley = models.CharField(max_length=50 , null=True , blank=True)
    plaque = models.CharField(max_length=50)
        