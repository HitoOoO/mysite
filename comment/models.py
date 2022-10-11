from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import threading
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import render
# Create your models here.

class SendMail(threading.Thread):

    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    root = models.ForeignKey('self',related_name="root_comment",null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name="parent_comment",null=True,on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User,related_name="replies",null=True,on_delete=models.CASCADE)

    def send_mail(self):
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的博客'
            email = self.user.email
        else:
            # 回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
            print(email)
        if email != '':
            context = {}
            context['comment_text'] = self.text
            text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
            send_mail = SendMail(subject,text,email)
            send_mail.start()

    def __str__(self):
        return self.text
    class Meta:
        ordering = ['comment_time']