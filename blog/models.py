from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNumExpandMethod,ReadDetail
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
#博客类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

#博客
class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '<Blog: {}>'.format(self.title)

    def get_url(self):
        return reverse('Blog_detail', kwargs={'blog_id': self.id})

    def get_email(self):
        return self.author.email

    #分页排序
    class Meta:
        ordering = ['created_time']
