from django.db import models

# Create your models here.
class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    name = models.CharField(max_length=30)
    show_name = models.CharField(max_length=30)
    url = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(default=STATUS_DRAFT, choices=STATUS_ITEMS)


class Advertise(models.Model):
    title = models.CharField(max_length=100)
    image_url = models.URLField()
    link_url = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)