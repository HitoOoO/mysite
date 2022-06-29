import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.id)
    if not request.COOKIES.get(key):  # 如果没有cookie 次数加一
        #总阅读数加1
        readnum,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)
        # 计数加1
        readnum.read_num += 1
        readnum.save()

        #当天阅读数加1
        date = timezone.now().date()
        readDetail,created= ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.id,date=date)
        readDetail.read_num +=1
        readDetail.save()

    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums=[]
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)  # 日期差量
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date = date)
        result = read_details.aggregate(read_num_sum = Sum('read_num'))   #求和结果
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date = today).order_by('-read_num')  #筛选完排序
    return read_details
