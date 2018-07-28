from django.conf.urls import url, include

from . import views
app_name = 'mfa'
# security_patterns = ([
#     url(r'^security/$', views.security_settings, name='security_settings'),
#     url(r'^mfa/configure/%', views.configure_mfa, name='configure_mfa'),
#     url(r'^mfa/enable/$', views.enable_mfa, name='enable_mfa'),
#     url(r'^verify/token/$', views.verify_otp, name='verify_otp'),
#     url(r'^mfa/disable/$', views.disable_mfa, name='disable_mfa'),
# ], 'mfa')

urlpatterns = [
    # url(r'^auth$/', include(security_patterns)),

    url(r'^security/$', views.security_settings, name='security_settings'),
    url(r'^mfa/configure/$', views.configure_mfa, name='configure_mfa'),
    url(r'^mfa/enable/$', views.enable_mfa, name='enable_mfa'),
    url(r'^verify/token/$', views.verify_otp, name='verify_otp'),
    url(r'^mfa/disable/$', views.disable_mfa, name='disable_mfa'),
]
