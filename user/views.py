from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegForm , ChangeNicknameForm , BindEmailForm , ChangePasswordForm ,ForgotPasswordForm
from django.contrib import auth
from django.http import JsonResponse
from .models import Profile
from django.core.mail import send_mail
import string
import random
import time
class Login(View):
    TEMPLATE = 'user/login.html'
    def get(self,request):
        login_form = LoginForm()
        context = {}
        context['login_form'] = login_form
        return render(request,self.TEMPLATE,context)
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
        context = {}
        context['login_form'] = login_form
        return render(request, self.TEMPLATE, context)
class Logout(View):
    def get(self,request):
        auth.logout(request)
        return redirect(request.GET.get('from', reverse('home')))
class User_info(View):
    TEMPLATE = 'user/user_info.html'
    def get(self,request):
        context = {}
        return render(request,self.TEMPLATE,context)
class Login_for_modal(View):
    def post(self,request):
        login_form = LoginForm(request.POST)
        data = {}
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
        return JsonResponse(data)
class Register(View):
    TEMPLATE = 'user/register.html'
    def get(self,request):
        reg_form = RegForm()
        context = {}
        context['reg_form'] = reg_form
        return render(request, self.TEMPLATE, context)
    def post(self,request):
        reg_form = RegForm(request.POST,request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            #清除session
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

        context = {}
        context['reg_form'] = reg_form
        return render(request, self.TEMPLATE, context)
class Change_nickname(View):
    TEMPLATE = 'form.html'
    def get(self,request):
        redirect_to = request.GET.get('from', reverse('home'))
        form = ChangeNicknameForm()
        context = {}
        context['page_title'] = '修改昵称'
        context['form_title'] = '修改昵称'
        context['submit_text'] = '修改'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request,self.TEMPLATE,context)
    def post(self,request):
        redirect_to = request.GET.get('from', reverse('home'))
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)

class Bind_email(View):
    TEMPLATE = 'user/bind_email.html'

    def post(self,request):
        redirect_to = request.GET.get('from', reverse('home'))
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
        context = {}
        context['page_title'] = '绑定邮箱'
        context['form_title'] = '绑定邮箱'
        context['submit_text'] = '绑定'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request, self.TEMPLATE, context)
    def get(self, request):
        redirect_to = request.GET.get('from', reverse('home'))
        form = BindEmailForm()
        context = {}
        context['page_title'] = '绑定邮箱'
        context['form_title'] = '绑定邮箱'
        context['submit_text'] = '绑定'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request, self.TEMPLATE, context)

class Send_verification_code(View):

    def get(self,request):
        email = request.GET.get('email', '')
        send_for = request.GET.get('send_for','')
        data = {}
        if email != '':
            #生成验证码
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            now = int(time.time())
            send_code_time = request.session.get('send_code_time', 0)
            if now - send_code_time < 30:
                data['status'] = 'ERROR'
            else:
                request.session[send_for] = code
                request.session['send_code_time'] = now
                #发送邮件
                send_mail(
                    '绑定邮箱验证码',   #邮箱主题
                    '验证码:{}'.format(code),  #内容
                    '1412335438@qq.com',
                    [email],
                    fail_silently=False,     #是否忽略
                )
                data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
        return JsonResponse(data)


class Change_password(View):
    TEMPLATE = 'form.html'

    def get(self, request):
        redirect_to = reverse('home')
        form = ChangePasswordForm()
        context = {}
        context['page_title'] = '修改密码'
        context['form_title'] = '修改密码'
        context['submit_text'] = '修改'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request, self.TEMPLATE, context)

    def post(self, request):
        redirect_to = reverse('home')
        form = ChangePasswordForm(request.POST, user=request.user)
        context={}
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
        context['page_title'] = '修改密码'
        context['form_title'] = '修改密码'
        context['submit_text'] = '修改'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request, self.TEMPLATE, context)


class Forgot_password(View):
    TEMPLATE = 'user/forgot_password.html'


    def post(self,request):
        redirect_to = reverse('login')
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
        context = {}
        context['page_title'] = '重置密码'
        context['form_title'] = '重置密码'
        context['submit_text'] = '重置'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request, self.TEMPLATE, context)
    def get(self,request):
        redirect_to = reverse('login')
        form = ForgotPasswordForm()

        context = {}
        context['page_title'] = '重置密码'
        context['form_title'] = '重置密码'
        context['submit_text'] = '重置'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request, self.TEMPLATE, context)
