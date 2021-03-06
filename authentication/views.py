from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .forms import UserCreationForm
# captcha
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import Captcha
import random
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

from django.conf import settings
from django.contrib.auth.decorators import login_required
from mfa_ggauth.models import is_mfa_enabled, UserOTP
from mfa_ggauth import totp

def random_id():
    return random.randint(1,7)
class LoginView(base_auth_views.LoginView):

    def get_context_data(self, **kwargs):
        id_ = random_id()
        cap = Captcha.objects.get(id=id_)
        context = super().get_context_data(**kwargs)
        context['cap'] = cap
        context['id_'] = id_

        return context
    def form_valid(self, form):
        id_ = self.request.POST['captcha_id']
        cap = Captcha.objects.get(id=id_)
        get_code_captcha = self.request.POST['code_captcha']
        # recaptcha_response = self.request.POST.get('g-recaptcha-response')
        # data = {
        #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        #
        # # without ssl certificat check
        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, verify=False)
        #
        # # with ssl certificat check
        # # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        #
        # result = r.json()
        if get_code_captcha == cap.code_captcha:
            # messages.success(self.request, 'login success!')
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())

        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
        return redirect('registration:login1')


def SignUp(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        cap = Captcha.objects.get(id=random_id())
        print("Cap = ", cap)

        if form.is_valid():
            get_code_captcha = request.POST['code_captcha']
            print("cap " ,cap)
            if get_code_captcha == cap.code_captcha:
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
        # print("random = ", random)
        cap = Captcha.objects.get(id=random_id())
        print("Cap = ", cap)
    return render(request, 'signup.html',{'form':form,
                                            'cap':cap,
                                            })

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
        user_ = models.User.objects.all()
        context = super().get_context_data(**kwargs)
        context['user_'] = user_
        return context

def IndexView(request, username):
    user = User.objects.get(username = username) #user dang duoc xem profile
    if request.user == user:
    	check_login = True
    else:
    	check_login = False
    if not check_login :#anonymous
    	try:
            content_field = request.POST['content_']
            asker_field = request.POST['asker_']
            verification_code = request.POST['verification_code']
            is_verified = False
            print('cau hoi: ',content_field)
            print('ma xac thuc: ',verification_code)
            if verification_code is None:
                messages.error(request, 'You need to type the code!')
                print(" chua nhap ma")
            else:
                print("is_verified ???", is_verified)
                print(" da nhap ma code")
                print("user = ", request.user)
                print("secret_key = ", UserOTP.secret_key)
                if not is_mfa_enabled(request.user):
                    messages.error(request, 'You have to enable google authenticator to ask someone!')
                    print(" chua bat 2 buoc")
                else:
                    otp_ = UserOTP.objects.get(user=request.user)
                    print("key = ", otp_.secret_key)
                    #  key =  OW4B3JUVNOAJJVYK
                    #logout ra, dang nhap lai thi key cua user van giu nguyen, do bang UserOTP k thay đổi
                    totp_ = totp.TOTP(otp_.secret_key)
                    print("opt_   = ", otp_ )
                    print("topt_   = ", totp_)
                    is_verified = totp_.verify(verification_code)
                    print(totp_.verify(verification_code))
                    print("is_verified ???", is_verified)
                    """
                    user =  vlc1
                secret_key =  <django.db.models.query_utils.DeferredAttribute object at 0x7fca82acab00>
                key =  45RGJD2XTIYPKXWB
                opt_   =  UserOTP object
                topt_   =  <mfa_ggauth.totp.TOTP object at 0x7fca8060f0f0>

                    """

                    if  is_verified:
                        # request.session['verfied_otp'] = True
                        user.question_ahihi.create(content = content_field,
                		 name_asker = asker_field,
                    	 id_user_receive_id = user.id,
                     	 answer ="")
                        messages.success(request, 'You just asked!!!')
                    else:
                        messages.error(request, 'Your code is expired or invalid')
            return HttpResponseRedirect(reverse('registration:index', args = (username, )))
    	except:

            try:
                question_list = user.question_ahihi.filter(id_user_receive_id = user.id).all()
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
    	try:
            verification_code = request.POST['verification_code']
            is_verified = False
            answer_field = request.POST['answer_']
            question_id = request.POST['question_id']
            if not is_mfa_enabled(request.user):
                messages.error(request, 'You have to enable google authenticator to ask someone!')
                print(" chua bat 2 buoc")
            else:

                otp_ = UserOTP.objects.get(user=request.user)
                print("key = ", otp_.secret_key)
                #  key =  OW4B3JUVNOAJJVYK
                #logout ra, dang nhap lai thi key cua user van giu nguyen, do bang UserOTP k thay đổi
                totp_ = totp.TOTP(otp_.secret_key)
                print("opt_   = ", otp_ )
                print("topt_   = ", totp_)
                is_verified = totp_.verify(verification_code)
                print(totp_.verify(verification_code))
                print("is_verified ???", is_verified)
                """
                user =  vlc1
            secret_key =  <django.db.models.query_utils.DeferredAttribute object at 0x7fca82acab00>
            key =  45RGJD2XTIYPKXWB
            opt_   =  UserOTP object
            topt_   =  <mfa_ggauth.totp.TOTP object at 0x7fca8060f0f0>

                """

                if is_verified:
                    answer_pickup = user.question_ahihi.get(pk = question_id)
                    answer_pickup.answer = answer_field
                    answer_pickup.save()
                    # messages.success(request, 'You just answered!!!')
                else:
                    messages.error(request, 'Your code is expired or invalid')
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
