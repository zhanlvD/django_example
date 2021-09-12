import datetime

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from apps.bloguser.decorators import peekpa_login_superuser_required
from apps.bloguser.models import User, UserVisit, DailyVisitNum, TotalVisitNum
from apps.link.models import Link, Advertise
from apps.post.models import Category, Post

from utils.paginator_helper import get_paginator, get_pagination_data


def cms_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('cms:dashboard'))
    return render(request, 'cms/login.html')


@login_required
def cms_dashboard(request):
    context = {}
    context.update(get_dashboard_top_data())
    context.update(get_dashboard_visitor_chart())
    context.update(get_advertise())
    context.update(get_visitor_table(10))
    context.update(get_post_table(10))
    return render(request, 'cms/dashboard/home.html', context=context)


def get_post_table(max_num):
    visitor_day_data = UserVisit.objects.filter(day=datetime.datetime.now().strftime('%Y-%m-%d'), end_point__contains='/detail/')
    post_map = {}
    post_view_table_list = []
    if visitor_day_data:
        for item in visitor_day_data:
            post_id = item.end_point.split('/')[2]
            if post_id in post_map:
                post_map[post_id] += 1
            else:
                post_map[post_id] = 1
    if post_map:
        for key in post_map:
            key = key
            post_item = Post.objects.filter(time_id=key)
            if post_item:
                post_item[0].inscrease = post_map[key]
                post_view_table_list.append(post_item[0])
    if post_view_table_list:
        post_view_table_list.sort(key=lambda x: x.inscrease, reverse=True)
    if max_num > 0 and len(post_view_table_list) > max_num:
        post_view_table_list = post_view_table_list[:max_num]
    context = {
        'post_view_table_list': post_view_table_list,
    }
    return context


def get_visitor_table(max_num):
    visitor_data = UserVisit.objects.all().order_by('-day')
    if len(visitor_data):
        visitor_data = visitor_data[:max_num]
    context = {
        'visitor_data_list': visitor_data,
    }
    return context

def get_advertise():
    advertise_link = Advertise.objects.all()[0] if Advertise.objects.all().count() else None
    context = {
        'advertise_link': advertise_link
    }
    return context

def get_dashboard_top_data():
    post_num = Post.objects.all().count()
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    day_visit_ip_set = set()
    day_visit_ip_list = UserVisit.objects.filter(day=cur_date)
    if day_visit_ip_list:
        for user_ip_item in day_visit_ip_list:
            if user_ip_item.ip_address not in day_visit_ip_set:
                day_visit_ip_set.add(user_ip_item.ip_address)
    day_visit_ip_num = len(day_visit_ip_set)
    day_visit_num = DailyVisitNum.objects.filter(day=cur_date)[0].count if DailyVisitNum.objects.filter(day=cur_date).count() else 0
    total_visit_num = TotalVisitNum.objects.all()[0].count if TotalVisitNum.objects.all().count() else 0
    context = {
        "post_num": post_num,
        "day_visit_ip_num": day_visit_ip_num,
        "day_visit_num": day_visit_num,
        "total_visit_num": total_visit_num
    }
    return context

def get_dashboard_visitor_chart():
    this_week_visit_list = []
    last_week_visit_list = []
    max_num = 0
    week_total_num = 0
    cur_day_in_week = datetime.datetime.today().weekday()
    for index in range(cur_day_in_week, -1, -1):
        day_format_string = get_before_date(index)
        day_visit_num = 0
        daynumber_item = DailyVisitNum.objects.filter(day=day_format_string)
        if daynumber_item:
            day_visit_num = daynumber_item[0].count
        this_week_visit_list.append(day_visit_num)
        week_total_num += day_visit_num
        max_num = day_visit_num if day_visit_num > max_num else max_num
    for index in range(cur_day_in_week + 7, cur_day_in_week, -1):
        day_format_string = get_before_date(index)
        day_visit_num = 0
        daynumber_item = DailyVisitNum.objects.filter(day=day_format_string)
        if daynumber_item:
            day_visit_num = daynumber_item[0].count
        last_week_visit_list.append(day_visit_num)
    max_num = 50 if max_num < 50 else max_num
    context = {
        'visit_week_total_number': week_total_num,
        'this_week_data_list': this_week_visit_list,
        'last_week_data_list': last_week_visit_list,
        'suggested_max': max_num
    }
    return context

def get_before_date(day):
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-day)
    re_date = (today + offset).strftime("%Y-%m-%d")
    return re_date

@login_required
def category_manage_view(request):
    context = {
        "list_data": Category.objects.all()
    }
    return render(request, 'cms/category/manage.html', context=context)

@login_required
def category_publish_view(request):
    return render(request, 'cms/category/publish.html')


@login_required
def post_manage_view(request):
    page = int(request.GET.get('p', 1))
    posts = Post.objects.all()
    paginator = get_paginator(posts)
    page_obj = paginator.page(page)
    context = {
        "list_data": page_obj.object_list,
        'list_data_status': Post.STATUS_ITEMS
    }
    context.update(get_pagination_data(paginator, page_obj))
    return render(request, 'cms/post/manage.html', context=context)


@login_required
def post_publish_view(request):
    context = {
        'list_data_category': Category.objects.all(),
        'list_data_user': User.objects.all(),
        'list_data_status': Post.STATUS_ITEMS
    }
    return render(request, 'cms/post/publish.html', context=context)


@login_required
def link_manage_view(request):
    context = {
        "list_data": Link.objects.all(),
        'list_data_status': Link.STATUS_ITEMS
    }
    return render(request, 'cms/link/manage.html', context=context)


@login_required
def link_publish_view(request):
    context = {
        'list_data_status': Link.STATUS_ITEMS
    }
    return render(request, 'cms/link/publish.html', context=context)

@login_required
def advertise_manage_view(request):
    context = {
        "list_data": Advertise.objects.all()
    }
    return render(request, 'cms/advertise/manage.html', context=context)


@login_required
def advertise_publish_view(request):
    return render(request, 'cms/advertise/publish.html')

@login_required
@peekpa_login_superuser_required
def user_manage_view(request):
    context = {
        "list_data": User.objects.all(),
    }
    return render(request, 'cms/user/manage.html', context=context)

@login_required
@peekpa_login_superuser_required
def user_publish_view(request):
    return render(request, 'cms/user/publish.html')