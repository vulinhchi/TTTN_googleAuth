from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings


from django.contrib.auth import views as auth_views # su dung login, logout mac dinh
from . import views
app_name = 'registration'
urlpatterns =[
    url(r'^signup/$', views.SignUp, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^login/$', views.LoginView.as_view(), name='login1'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^list/$', views.ListUser.as_view(), name='listuser'),
    url(r'^ask/(?P<username>.+)/$', views.IndexView, name='index'),
    # url(r'^detailuser/(?P<slug>.+)/$', views.DetailProfileView.as_view() , name='detailuser'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
