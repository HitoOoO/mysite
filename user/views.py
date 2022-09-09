from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegForm , ChangeNicknameForm
from django.contrib import auth
from django.http import JsonResponse
from .models import Profile

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
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
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
