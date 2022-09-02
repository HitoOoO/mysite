"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from blog import urls as blog_urls
from comment import urls as comment_urls
from likes import urls as likes_urls
from mysite.views import Home,Login,Register,Login_for_modal
from django.conf import settings
from django.conf.urls.static import static
from . import views
from blog.views import Blog_list
urlpatterns = [
    path('',Home.as_view(),name = 'home'),
    path('admin/', admin.site.urls),
    path('blog/',include(blog_urls)),
    path('comment/',include(comment_urls)),
    path('likes/',include(likes_urls)),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('login/',Login.as_view(),name = 'login'),
    path('login_for_modal/',Login_for_modal.as_view(),name ='login_for_modal'),
    path('register/',Register.as_view(),name = 'register'),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
