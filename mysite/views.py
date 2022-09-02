from django.views.generic import View
from django.shortcuts import render,redirect
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_7_days_hot_blogs
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegForm
from django.contrib import auth
from django.http import JsonResponse
class Home(View):
    TEMPLATE = 'home.html'
    def get(self,request):
        blog_content_type = ContentType.objects.get_for_model(Blog)
        dates,read_nums = get_seven_days_read_data(blog_content_type)
        #获取七天热门博客缓存的数据
        hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
        if hot_blogs_for_7_days is None:
            hot_blogs_for_7_days = get_7_days_hot_blogs()
            cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days,3600)

        context = {}
        context['read_nums'] = read_nums
        context['dates'] = dates
        context['today_hot_data'] = get_today_hot_data(blog_content_type)
        context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
        context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
        return render(request,self.TEMPLATE,context)

class Login(View):
    TEMPLATE = 'login.html'
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
    TEMPLATE = 'register.html'
    def get(self,request):
        reg_form = RegForm()
        context = {}
        context['reg_form'] = reg_form
        return render(request, 'register.html', context)
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


