from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType      #应用模型
from django.db.models.fields import exceptions
from django.utils import timezone

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)         #外键指向contenttype模型
    object_id = models.PositiveIntegerField()                                       #作为主键值
    content_object = GenericForeignKey('content_type', 'object_id')                     #把上面俩变成通用外键

class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct,object_id=self.id)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0