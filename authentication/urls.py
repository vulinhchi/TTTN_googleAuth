from django.urls import path
from django.contrib.auth import views as auth_views # su dung login, logout mac dinh
from . import views
app_name = 'registration'
urlpatterns =[
    path('signup', views.SignUp, name='signup'),
    path('confirm/<uidb64>/<token>', views.activate, name='activate'),
    path('login', views.LoginView.as_view(), name='login1'),
    path('logout', auth_views.LogoutView.as_view(), name='logout')
]
