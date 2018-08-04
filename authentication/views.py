from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .forms import UserCreationForm
# captcha
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
#captcha

from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from . import models
from django.views import generic

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
# authenticator
import base64
import codecs
import random
import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from mfa_ggauth.models import is_mfa_enabled, UserOTP

from mfa_ggauth import totp
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



class ListUser(generic.ListView):
    template_name = 'listuser.html'# list ra cac profile tru Admin
    model = models.User
    def get_context_data(sefl, **kwargs):
        user_ = models.User.objects.all
        context = super().get_context_data(**kwargs)
        context['user_'] = user_
        return context

# def IndexView(request, username):
#     ctx = {}
#     if request.method == "POST":
#         user = User.objects.get(username = username) #user hien dang dang nhap
#         if request.user == user:
#         	check_login = True
#         else:
#         	check_login = False
#
#         if not check_login:
#             content_field = request.POST['content_']
#             asker_field = request.POST['asker_']
#
#             user.question_ahihi.create(content = content_field,
#              name_asker = asker_field,
#              id_user_receive_id = user.id,
#              answer ="")
#
#             question_list = user.question_ahihi.filter(id_user_receive_id = user.id).all()
#             return render(request, 'index.html',ctx,
#          			{'question_list': question_list,
#                  	'username': user.username,
#                  	'first_name': user.first_name,
#                  	'last_name': user.last_name,
#                  	'check_login':check_login})
#
#         else: # if check_login
#             answer_field = request.POST['answer_']
#             question_id = request.POST['question_id']
#             answer_pickup = user.question_ahihi.get(pk = question_id)
#             answer_pickup.answer = answer_field
#             answer_pickup.save()
#             question_list = user.question_ahihi.filter(id_user_receive_id = user.id).all()
#             return render(request, 'index.html',ctx,
#          			{'question_list': question_list,
#                  	'username': user.username,
#                  	'first_name': user.first_name,
#                  	'last_name': user.last_name,
#                  	'check_login':check_login})
#     return render(request, 'index.html',ctx)



def IndexView(request, username):
    user = User.objects.get(username = username) #user hien dang dang nhap
    ctx = {}
    if request.user == user:
    	check_login = True
    else:
    	check_login = False
    if not check_login :#anonymous
    	# anonymous can ask
    	try:

            content_field = request.POST['content_']
            asker_field = request.POST['asker_']
            verification_code = request.POST['verification_code']
            is_verified = False
            print('cau hoi: ',content_field)
            print('ma xac thuc: ',verification_code)
            if verification_code is None:
                messages.success(request, 'Missing verification code.')
                print(" chua nhap ma")
            else:
                print("is_verified ???", is_verified)
                print(" da nhap ma code")
                print("user = ", request.user)
                print("secret_key = ", UserOTP.secret_key)
                otp_ = UserOTP.objects.get(user=request.user)
                totp_ = totp.TOTP(otp_.secret_key)
                print("opt_   = ", otp_ )
                print("topt_   = ", totp_)
                is_verified = totp_.verify(verification_code)
                print("is_verified ???", is_verified)

                if  is_verified:
                    # request.session['verfied_otp'] = True
                    user.question_ahihi.create(content = content_field,
            		 name_asker = asker_field,
                	 id_user_receive_id = user.id,
                 	 answer ="")
                    # return HttpResponseRedirect(request.POST.get("next", settings.LOGIN_REDIRECT_URL))
                message.error(request,"Your code is expired or invalid.")
                error_message= "Your code is expired or invalid."
            return HttpResponseRedirect(reverse('registration:index' ,args = (username,error_message )))
    	except:

            try:
                question_list = user.question_ahihi.filter(id_user_receive_id = user.id).all()
                #loc ra danh sach cac cau hoi theo user

            except:
                pass
            return render(request, 'index.html',
    			{'question_list': question_list,
            	'username': user.username,
            	'first_name': user.first_name,
            	'last_name': user.last_name,
            	'check_login':check_login,

                })
    else: #current user
    	#error = "you have to log in first!"
    	#return render(request, 'authentication/login.html',{"error":error})
    	try:

    		answer_field = request.POST['answer_']
    		question_id = request.POST['question_id']
    		answer_pickup = user.question_ahihi.get(pk = question_id)
    		answer_pickup.answer = answer_field
    		answer_pickup.save()
    		return HttpResponseRedirect(reverse('registration:index', args = (username, )))
    	except:
    		try:
    			question_list = user.question_ahihi.filter(id_user_receive_id = user.id).all()
    		#loc ra danh sach cac cau hoi theo user
    		except:
    			pass
    		return render(request, 'index.html',
    		{'question_list': question_list,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'check_login':check_login})
