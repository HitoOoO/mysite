from django.views.generic import View
from django.shortcuts import render_to_response
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
class Home(View):
    TEMPLATE = 'home.html'
    def get(self,request):
        blog_content_type = ContentType.objects.get_for_model(Blog)
        dates,read_nums = get_seven_days_read_data(blog_content_type)
        today_hot_data = get_today_hot_data(blog_content_type)
        context = {}
        context['read_nums'] = read_nums
        context['dates'] = dates
        context['today_hot_data'] = today_hot_data
        return render_to_response(self.TEMPLATE,context)
