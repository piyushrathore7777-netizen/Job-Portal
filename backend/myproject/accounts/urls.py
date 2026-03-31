from django.urls import path
from .views import register,login,company_login,company_register,post_job

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('company/register/',company_register),
    path('company/login/',company_login),
    path('company/post-job/',post_job),
]