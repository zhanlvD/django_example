from django.shortcuts import render
import markdown
# Create your views here.
from apps.bloguser.tracking import peekpa_tracking
from apps.link.models import Link, Advertise
from apps.post.models import Post
from django.core.cache import cache
from django.db.models import F


@peekpa_tracking
def index(request):
    top_post = Post.objects.filter(status=Post.STATUS_NORMAL, priority__gt=0).order_by('-priority')
    if len(top_post) > 4:
        top_post = top_post[:4]
    list_post = Post.objects.filter(status=Post.STATUS_NORMAL, priority=0)
    context = {
        'top_post': top_post,
        'list_post': list_post
    }
    context.update(get_read_most_post())
    context.update(get_link())
    context.update(get_advertise())
    return render(request, 'post/index.html', context=context)


@peekpa_tracking
def post_list_view(request):
    hot_post = Post.objects.filter(status=Post.STATUS_NORMAL, is_hot=True).order_by('time_id')
    list_post = Post.objects.filter(status=Post.STATUS_NORMAL, is_hot=False).order_by('time_id')
    context = {
        'hot_post': hot_post,
        'list_post': list_post,
    }
    context.update(get_read_most_post())
    context.update(get_link())
    context.update(get_advertise())
    return render(request, 'post/list.html', context=context)

@peekpa_tracking
def detail(request, time_id):
    post = Post.objects.select_related('category', 'author').get(time_id=time_id)
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
    # post.content_html = md.convert(post.content)
    md.convert(post.content)
    context = {
        'post_data': post,
        'toc': process_toc(md.toc)
    }
    context.update(get_read_most_post())
    context.update(get_link())
    context.update(get_advertise())
    handle_visited_num(request, time_id)
    return render(request, 'post/detail.html', context=context)


def get_read_most_post():
    read_post = Post.objects.all().order_by('-read_num')
    if len(read_post) > 5:
        read_post = read_post[:5]
    context = {
        'read_post': read_post
    }
    return context

def get_link():
    links = Link.objects.filter(status=Link.STATUS_NORMAL)
    context = {
        'link_data': links
    }
    return context

def get_advertise():
    advertise_link = Advertise.objects.all()[0] if Advertise.objects.all().count() else None
    context = {
        'advertise_link': advertise_link
    }
    return context

def process_toc(toc):
    toc = toc.replace('<div class="toc">', '').replace('</div>','').replace('<ul>','<ul class="list-group">').replace('<li>','<li class="border-0 list-group-item ">')
    if len(toc) <= 31:
        toc = None
    return toc


def handle_visited_num(request, time_id):
    increase_post_view = False
    uid = request.uid
    pv_key = 'pv:%s:%s' % (uid, request.path)
    if not cache.get(pv_key):
        increase_post_view = True
        cache.set(pv_key, 1, 2 * 60)
    if increase_post_view:
        Post.objects.filter(time_id=time_id).update(read_num=F('read_num') + 1)