import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum


def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.id)
    if not request.COOKIES.get(key):  # 如果没有cookie 次数加一
        if ReadNum.objects.filter(content_type=ct, object_id=obj.id).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.id)
        else:
            # 不存在对应记录
            readnum = ReadNum(content_type=ct, object_id=obj.id)
        # 计数加1
        readnum.read_num += 1
        readnum.save()
    return key