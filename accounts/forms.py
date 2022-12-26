from django.forms import ModelForm,ValidationError,Form
from django.forms.fields import CharField
from django.forms.widgets import (PasswordInput,EmailInput,TextInput)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
User=get_user_model()

# used in admin site
class UserAdminCreationForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Password confirmation', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("password_mismatch")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# used in admin site
class UserAdminChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_superuser','is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

# login form
class LoginForm(Form):
  username=CharField(widget=TextInput(attrs={"placeholder":"Username","class":"form-input"}))
  password=CharField(widget=PasswordInput(attrs={"placeholder":"Password","class":"form-input"}))

# register form
class RegisterForm(ModelForm):
  class Meta:
    model=User
    fields=['username','email','password','dp']
    widgets={
            'username':TextInput(attrs={"placeholder":"Username","class":"form-input"}),
            'email':EmailInput(attrs={"placeholder":"Email","class":"form-input"}),
            'password':PasswordInput(attrs={"placeholder":"Password","class":"form-input"}),
    }

# change password form
class PassWordChangeForm(Form):
    password1=CharField(label="old password",widget=PasswordInput(attrs={"placeholder":"old password","class":"form-input"}))
    password2=CharField(label="new password",widget=PasswordInput(attrs={"placeholder":"new password","class":"form-input"}))

# send password reset mail form
class SendPasswordResetMailForm(Form):
    email=CharField(widget=EmailInput(attrs={'placeholder':'your email'}))

# reset password form
class ResetPassWordForm(Form):
    password=CharField(widget=PasswordInput(attrs={'placeholder':'set new password'}))

# update user profile
class UpdateForm(ModelForm):
  class Meta:
    model=User
    fields=['dp','name']
    widgets={
            'email':EmailInput(attrs={"placeholder":"Email","class":"form-input"}),
            'name':TextInput(attrs={"placeholder":"Name","class":"form-input"}),
    }