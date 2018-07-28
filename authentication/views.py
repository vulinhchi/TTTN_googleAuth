from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from .forms import UserCreationForm
# captcha
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
#captcha
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from . import models

from django.contrib.auth import views as base_auth_views
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import get_object_or_404

def index(request):
    if request.user and request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            login(request, form.user)
            return JsonResponse({"error": False})
        else:
            return JsonResponse({"error": True, "errors": form.errors})
    context = {

        "login_form": AuthenticationForm
    }
    return render(request, 'registration/login.html', context)

class LoginView(base_auth_views.LoginView):

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }

        # without ssl certificat check
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, verify=False)

        # with ssl certificat check
        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)

        result = r.json()
        if result['success']:
            messages.success(self.request, 'login success!')
            # return HttpResponseRedirect('registration:ggauth')
            # return redirect('registration:signup')
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())

        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
        return redirect('registration:login1')


def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # check recaptcha truoc
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }

            # without ssl certificat check
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, verify=False)

            # with ssl certificat check
            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)

            result = r.json()
            if result['success']:
                messages.success(request, 'sign up success! Please check your email to complete the registration!')
                user = form.save(commit=False)
                user.is_active = False
                user.save()# thong tin user van duoc luu, nhung chua duoc ACTIVE
                current_site = get_current_site(request)
                mail_subject = 'Activate your account!'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                })
                print ("ahihihihih: ",account_activation_token.make_token(user))
                #to_email = form.cleaned_data.get('email')
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                # return HttpResponse('Please confirm your email address to complete the registration')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
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

#add google Authenticator
