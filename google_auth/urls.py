
from django.contrib import admin
from django.conf.urls import url, include

from django.views.generic.base import TemplateView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mfa/',include('mfa_ggauth.urls')),
    url(r'^accounts/', include('authentication.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', TemplateView.as_view(template_name='base.html'), name='home'),
    #path('index', TemplateView.as_view(template_name='registration/login.html'), name='index'),
]
