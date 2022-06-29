from django.contrib import admin
from .models import ReadNum,ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')

@admin.register(ReadDetail)
class ReadDetail(admin.ModelAdmin):
    list_display = ('date','read_num', 'content_object')

