from django.shortcuts import render,render_to_response,get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from .models import Blog,BlogType
from django.conf import settings
from django.db.models import Count
from datetime import datetime

def get_blog_list_common_data(request,blogs_all_list):

    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每页显示5条,根据setting里的EACH_PAGE_BLOGS_NUMBER设置
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num)  # 获取当前页码的数据
    current_page_num = page_of_blogs.number  # 获取当前页码
    page_range = [x for x in range(current_page_num - 2, current_page_num + 3) if
                  0 < x <= paginator.num_pages]  # 获取当前页码前后两页的页码,并且判断是否越界
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上省略页码标记 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)

    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取博客分类的对应博客数量
    #BlogType.objects.annotate(blog_count=Count('blog'))
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''
    #获取日期归档对应的博客数量
    blog_dates=Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict ={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict

    return context

#首页
class Blog_list(View):
    TEMPLATE = 'Blog_list.html'
    def get(self,request):
        blogs_all_list = Blog.objects.all()
        context = get_blog_list_common_data(request,blogs_all_list)
        return render_to_response(self.TEMPLATE,context)
#分类页
class Blog_with_type(View):
    TEMPLATE = 'Blog_with_type.html'
    def get(self,request,blog_type_id):
        blog_type = get_object_or_404(BlogType,id=blog_type_id)
        blogs_all_list = Blog.objects.filter(blog_type=blog_type)
        context = get_blog_list_common_data(request,blogs_all_list)
        context['blog_type'] = blog_type

        return render_to_response(self.TEMPLATE,context)
#按时间分类
class Blog_with_date(View):
    TEMPLATE = 'Blog_with_date.html'
    def get(self,request,year,month):
        blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
        context = get_blog_list_common_data(request,blogs_all_list)
        context['blog_with_date'] = '{}年{}月'.format(year,month)
        return render_to_response(self.TEMPLATE, context)
#详情页
class Blog_detail(View):
    TEMPLATE = 'Blog_detail.html'
    def get(self,request,blog_id):
        context = {}
        blog = get_object_or_404(Blog,id=blog_id)
        if not request.COOKIES.get('blog_{}_readed'.format(blog_id)):
            blog.readed_num += 1   #每次打开阅读次数加1
            blog.save()
        context['blog'] = blog
        context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).last()
        context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).first()
        response = render_to_response(self.TEMPLATE,context)
        response.set_cookie('blog_{}_readed'.format(blog_id),'true')                             #max_age  多少时间过期
        return response

















