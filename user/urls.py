


from django.urls import path,include
from user.views import Login,Register,Login_for_modal,Logout,User_info,Change_nickname,Bind_email,Send_verification_code,Change_password,Forgot_password
from django.conf import settings
from django.conf.urls.static import static

from blog.views import Blog_list
urlpatterns = [
    path('login/',Login.as_view(),name = 'login'),
    path('logout/',Logout.as_view(),name = 'logout'),
    path('login_for_modal/',Login_for_modal.as_view(),name ='login_for_modal'),
    path('register/',Register.as_view(),name = 'register'),
    path('user_info/',User_info.as_view(),name = 'user_info'),
    path('change_nickname/',Change_nickname.as_view(),name ='change_nickname'),
    path('bind_email/',Bind_email.as_view(),name='bind_email'),
    path('send_verification_code/',Send_verification_code.as_view(),name='send_verification_code'),
    path('change_password/',Change_password.as_view(),name='change_password'),
    path('forgot_password/',Forgot_password.as_view(),name='forgot_password'),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
