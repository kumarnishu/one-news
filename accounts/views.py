from django.shortcuts import render,redirect
from django.urls import reverse_lazy 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from . import helpers
from django.utils import timezone
from django.views import generic
from . import forms 
import uuid

User=get_user_model()

#login user
class Login(generic.FormView):
    form_class=forms.LoginForm
    template_name="accounts/login.html"
    success_url=reverse_lazy("accounts:login")
    
    # handle get request
    def get(self, request):
      if request.user.is_authenticated:
        messages.info(self.request,"already logged in")
        return redirect("/")
      return render(request, self.template_name,{'form':forms.LoginForm})
    
    # handle post method
    def form_valid(self, form):
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(self.request, user)
            request = self.request
            next_ = request.GET.get('next')
            next_post = request.POST.get('next')
            redirect_path = next_ or next_post or "/"
            return redirect(redirect_path)
        messages.info(self.request,"invalid credentials")
        return super().form_valid(form)

#logout user
class Logout(LoginRequiredMixin,generic.FormView):  
    def get(self,request):
        logout(request)
        return redirect("accounts:login")
    def post(self,request):
        logout(request)
        return redirect("accounts:login")

 #register new user
class Register(generic.CreateView):
   model=User
   form_class=forms.RegisterForm
   template_name="accounts/register.html"
   success_url="/"
   def get(self, request):
      if request.user.is_authenticated:
        messages.info(self.request,"already logged in")
        return redirect("/")
      return render(request, self.template_name,{'form':forms.RegisterForm})
   def form_valid(self,form):
        user=form.save(commit=False)
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user=authenticate(username=username,password=password)
        login(self.request,user)
        return super().form_valid(form)

#user profile
class UserProfile(LoginRequiredMixin,generic.DetailView):
   model=User
   template_name="newsapp/profile.html"
   context_object_name ="profile"

#update user 
class Update(LoginRequiredMixin,generic.UpdateView):
   model=User
   form_class=forms.UpdateForm
   template_name="accounts/update.html"

#password change
class  PasswordChange(LoginRequiredMixin,generic.FormView):
  form_class=forms.PassWordChangeForm
  template_name="accounts/password_change.html"
  success_url="/"
  def form_valid(self,form):
    password1=form.cleaned_data['password1']
    password2=form.cleaned_data['password2']
    user=authenticate(username=self.request.user.username,password=password1)
    if user is not None:
      self.request.user.set_password(password2)
      self.request.user.save()
      messages.info(self.request,"password reset successful")
      return redirect("/")
    messages.info(self.request,"old password is incorrect")
    return render(self.request, self.template_name,{'form':forms.PassWordChangeForm})

#send password reset link
class  SendPasswordResetMail(generic.FormView):
  form_class=forms.SendPasswordResetMailForm
  template_name="accounts/password_reset_email.html"
  success_url=reverse_lazy("accounts:send_password_reset_mail")
  def form_valid(self, form):
      email=form.cleaned_data['email']
      user=User.objects.get(email=email)
      token=str(uuid.uuid4())
      helpers.send_password_reset_link(email,token)
      user.password_reset_token=token
      user.password_reset_token_expire=timezone.now()
      user.save()
      messages.info(self.request,"mail sent")
      return redirect("accounts:send_password_reset_mail")  

# pending view
class PasswordReset(generic.FormView):
    form_class=forms.ResetPassWordForm
    template_name="accounts/reset_password.html"
    success_url="/accounts"
    def form_vaid(self,form,*args,**kwargs):
        user=User.objects.filter(password_reset_token=self.kwargs['token'])
        print(user)
        messages.info(self.request,"password reset done")




