from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, get_user_model , authenticate, logout 

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail 

from adv_blog.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, TemplateView, DetailView, UpdateView
from .forms import LoginForm, SignUpForm, ProfileEditForm
from .tokens import activation_token 
# Create your views here.

USER  = get_user_model()
class UserLoginView(View):
    model = USER 
    form_class = LoginForm
    
    def get(self, request):
        return render(request, 'accounts/login.html', {'form':self.form_class})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password = password)
            if user:
                print('User Found')
                login(request, user)
                return  redirect('blog:blog-home')
            else:
                messages.warning(request, ('Please enter valid user datails.'))
                return redirect('accounts:login')
        return render(request,'accounts/login.html', {'form':form})

class UserSignupView(View):
    template_name = 'accounts/signup.html'
    def get(self, request):
        form =  SignUpForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            # USER(
            #     first_name = form.cleaned_data['first_name'],
            #     last_name = form.cleaned_data['last_name'],
            #     email = form.cleaned_data['email'],
                
            # )
            recepient_email = form.cleaned_data['email']
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(f'Uid is {uid}')
            message = render_to_string('accounts/email/activation_email.html',{
                'user' : user,
                'domain' : current_site.domain,
                'uid' : uid,
                'token' : activation_token.make_token(user),
            })
            send_mail(subject=email_subject, message=message, from_email=EMAIL_HOST_USER,recipient_list=[recepient_email,])
            messages.success(request,('Please confirm your email to activate your account.'))
            return HttpResponse('accounts:login')
        return render(request, self.template_name, {'form':form})

def UserLogoutView(request):
    logout(request)
    return redirect('accounts:login')

class UserProfileView(DetailView):
    model = USER 
    slug_field = 'username'
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

class UserProfileEditView(UpdateView):
    model = USER
    slug_field = 'username'
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    
    
    
    # def post(self, request, slug):
    #     form = self.form_class(request.POST or request.FILE)
    #     if form.is_valid():
    #         old_password = form.cleaned_data['old_password']
    #         new_password = form.cleaned_data['new_password2']
    #         user = self.model.objects.get(email=self.request.user.email)
    #         if user.check_password(raw_password=old_password) == True: 
    #             user.set_password(new_password) 
    #             user.save()
    #         else:
    #             print('Not valid passow')
    #         return redirect('accounts:profile',slug) 



class ActivateAccount(View):

    def get(self,request, uidb64, token):
        try:
            print(uidb64)
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = USER.objects.get(pk=uid)
            print(uid)
        except (TypeError, ValueError, OverflowError, USER.DoesNotExist):
            user = None 
            print('Except block ')
        
        if user is not None and activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True 
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been activated.'))
            return redirect('accounts:login')
        
        else:
            return HttpResponse('The confirmation link is expired. Please signup again')
