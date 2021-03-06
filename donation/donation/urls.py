"""donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from donation_app.views import LandingPage, AddDonation, Login, Register, Logout, Profile, DonationDetail,\
    ProfileSettings, Activation, RemindPasswordView, ResetPassword
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='index'),
    path('add_donation/', AddDonation.as_view(), name='add-donation'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('donation/<int:id>', DonationDetail.as_view()),
    path('edit/', ProfileSettings.as_view(), name='settings'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #     Activate.as_view(), name='activate'),
    # path('new-user/', Signup.as_view(), name='new-user'),
    path('activate/<uidb64>/<token>/', Activation.as_view(), name='activate'),
    path('remind_password/', RemindPasswordView.as_view(), name='remind-password'),
    path('reset_password/<uidb64>/<token>/', ResetPassword.as_view(), name='reset-password'),
]
