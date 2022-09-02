from django.urls import path
from . import views
from blog.views import Blog_list,Blog_detail,Blog_with_type,Blog_with_date
from mysite.views import Login_for_modal
urlpatterns = [
    #http://127.0.0.1:8000/blog/1
    path('',Blog_list.as_view(),name = 'Blog_list'),
    path('<int:blog_id>',Blog_detail.as_view(),name='Blog_detail'),
    path('type/<int:blog_type_id>',Blog_with_type.as_view(),name='Blog_with_type'),
    path('date/<int:year>/<int:month>',Blog_with_date.as_view(),name='Blog_with_date'),
]