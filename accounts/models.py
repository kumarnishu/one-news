from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from . import managers

class User(AbstractBaseUser,PermissionsMixin):
  username=models.CharField(max_length=155,unique=True)
  email=models.EmailField(max_length=155,unique=True)
  name=models.CharField(max_length=155,null=True,blank=True)
  dp=models.ImageField(upload_to="dp/images",null=True,blank=True)
  is_active=models.BooleanField(default=True)
  is_staff=models.BooleanField(default=False)
  is_superuser=models.BooleanField(default=False)
  last_login = models.DateTimeField(blank=True, null=True)
  last_updated=models.DateTimeField(blank=True, null=True)
  date_joined=models.DateTimeField("date joined", blank=True,null=True)
  password_reset_token=models.TextField(max_length=500,null=True,blank=True)
  password_reset_token_expire=models.DateTimeField(blank=True,null=True)
  
  USERNAME_FIELD='username'
  REQUIRED_FIELDS = ['email']
  EMAIL_FIELD='email'

  objects=managers.UserManager()
  
  def get_absolute_url(self,*args,**kwargs):
    return reverse('accounts:user-profile', kwargs={'pk': self.pk})
  def get_edit_url(self,*args,**kwargs):
    return reverse('accounts:update',kwargs={'pk':self.pk})
  

