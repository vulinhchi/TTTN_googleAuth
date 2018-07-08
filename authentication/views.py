from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserCreationForm

from django.urls import reverse_lazy, reverse
#from django.views import generic
#from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from . import models

#from django.contrib.auth import views as base_auth_views
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import get_object_or_404
def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()# thong tin user van duoc luu, nhung chua duoc ACTIVE
            current_site = get_current_site(request)
            mail_subject = 'Activate your account!'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                #'uid': user.id,
                'token':account_activation_token.make_token(user),
            })
            print ("ahihihihih: ",account_activation_token.make_token(user))
            #to_email = form.cleaned_data.get('email')
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html',{'form':form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()

        user = models.User.objects.get(id=uid)
        print (" TEN USER LA: " , user.username)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'success_active_email.html')
    else:
        return HttpResponse('Activation link is invalid', {user})
