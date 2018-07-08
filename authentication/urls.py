from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'registration'
urlpatterns =[
    path('signup', views.SignUp, name='signup'),
    path('confirm/<uidb64>/<token>', views.activate, name='activate'),
    #path('', auth_views.LoginView.as_view(), name='login'),
    #path('signup', auth_views.SignUpView.as_view(), name='signup'),
    #path('login', views.LoginView1.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout')
]
