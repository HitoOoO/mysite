from django.views.generic import View
from django.shortcuts import render_to_response
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_7_days_hot_blogs
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
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
        return render_to_response(self.TEMPLATE,context)

