import datetime

from django.db import models
import markdown
import random

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey('bloguser.User', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    content_html = models.TextField(blank=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.IntegerField(default=-1)
    is_hot = models.BooleanField(default=False)
    status = models.PositiveIntegerField(default=STATUS_DRAFT, choices=STATUS_ITEMS)
    publish_time = models.DateTimeField(auto_now_add=True)
    time_id = models.CharField(blank=True, max_length=30)
    read_num = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-publish_time']

    def save(self, *args, **kwargs):
        md = markdown.Markdown(
            extensions=[
                # 包含 缩写、表格等常用扩展
                'markdown.extensions.extra',
                # 语法高亮扩展
                'markdown.extensions.codehilite',
                # 目录扩展
                'markdown.extensions.toc',
            ]
        )
        self.content_html = md.convert(self.content)

        if not self.time_id or len(self.time_id) == 0:
            self.publish_time = datetime.datetime.now()
            self.time_id = self.publish_time.strftime("%Y%m%d") + str(random.randrange(999, 10000, 1))
        super().save(*args, **kwargs)