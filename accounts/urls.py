from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
   # profile management urls
   path("user/profile/<int:pk>",views.UserProfile.as_view(),name="user-profile"),
   path("update/<int:pk>",views.Update.as_view(),name="update"),
   # authentication urls
   path("login/",views.Login.as_view(),name="login"),
   path("logout/",views.Logout.as_view(),name="logout"),
   path("register/",views.Register.as_view(),name="register"),
   # password management urls
   path("password/change/<int:pk>",views.PasswordChange.as_view(),name="password_change"),
   path("send/password/reset/mail/",views.SendPasswordResetMail.as_view(),name="send_password_reset_mail"),
   path("password/reset/<str:token>",views.PasswordReset.as_view(),name="password_reset/"),
]
