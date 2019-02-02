from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import View



# Email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from painless.tokens import account_activation_token
from painless import mail_templates as mailify
from django.core.mail import send_mail
from django.core.mail import BadHeaderError

from .forms import SignInForm
from .forms import SignUpForm
from accounts.models import User

# Create your views here.

class SignOut(RedirectView):
    url = reverse_lazy("home:index")

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(SignOut, self).get(request, *args, **kwargs)


class SignIn(FormView):
    form_class = SignInForm
    title = 'ورود'
    template_name = 'registration/authentication.html'
    success_url = reverse_lazy("home:index")

    def post(self, request, *args):
        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            auth_login(request, user)
            return redirect('home:index')
        else:
            messages.warning(self.request, 'نام کاربری یا رمز عبور اشتباه است و یا حساب کاربریتان غیر فعال است.')
            return redirect('accounts:signin')


class SignUp(CreateView):
    model = settings.AUTH_USER_MODEL
    template_name = 'registration/authentication.html'
    form_class = SignUpForm


    def form_valid(self, form):
        
        # Saving Process
        user = form.save(commit = False)
        user.is_active = False
        user.save()

        # Mailing Process
        to_mail = form.cleaned_data['email']
        current_site = get_current_site(self.request)
        
        name = "{} {}".format(user.first_name, user.last_name)
        subject = "فعال سازی حساب کاربری"
        message = "به وب سایت ما خوش آمدید"

        context = {
            "username": name,
            "text": "لطفا بر روی کلید فعال سازی کلیک نمایید.",
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            "token": account_activation_token.make_token(user),
        }

        html_msg = mailify.get_html_message('activate.html', self.request, context)
        try:
            
            send_mail(subject, message, 'siyamak1981@gmail.com', [to_mail], html_message=html_msg)
        except BadHeaderError:
            messages.warning(self.request, 'ایمیل فعال سازی برای شما ارسال نشد، لطفا دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.')
            return redirect('accounts:signup')

        # Messageing Process
        messages.success(self.request, 'جهت فعال سازی حساب کاربریتان لطفا ایمیل خود را بررسی نمایید.')
        return redirect('accounts:signup')


class Activate(View):
    def get(self, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            auth_login(self.request, user)
            return redirect('home:index')
        else:
            messages.warning(self.request, 'متاسفانه حساب کاربری شما فعال سازی نشد. برای اطلاعات بیشتر با پشتیبانی تماس بگیرید.')
            return redirect('accounts:signin')


