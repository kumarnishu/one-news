from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
  # create user function
  def create_user(self, username,email,password=None,**extra_fields):
        if not username:
          raise ValueError("Users must have an username")
        if not email:
          raise ValueError("Users must have an email address")
        if not password:
          raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # change user password
        user.save(using=self._db)
        return user
  
  #  staffuser function
  def create_staffuser(self,username,email,password=None,**extra_fields):
    extra_fields.setdefault('is_staff',True)
    user=self.create_user(username, email,password,**extra_fields) 
    return user


#  superuser function
  def create_superuser(self,username,email,password=None,**extra_fields):
    extra_fields.setdefault('is_staff',True)
    extra_fields.setdefault('is_superuser',True)
    user=self.create_user(username,email,password,**extra_fields) 
    return user
