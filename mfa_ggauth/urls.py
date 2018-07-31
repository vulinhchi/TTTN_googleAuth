from django.conf.urls import url, include

from . import views
app_name = 'mfa'

urlpatterns = [
    url(r'^mfa/configure/$', views.configure_mfa, name='configure_mfa'),
    url(r'^mfa/enable/$', views.enable_mfa, name='enable_mfa'),
    url(r'^verify/$', views.verify_otp, name="verify_otp"),
    url(r'^mfa/disable/$', views.disable_mfa, name='disable_mfa'),
]
