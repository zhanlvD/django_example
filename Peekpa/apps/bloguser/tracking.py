import datetime
from django.db.models import F
from apps.bloguser.models import TotalVisitNum, UserVisit, DailyVisitNum


def peekpa_tracking(func):
    def wrapper(request, *args, **kwargs):
        tacking_request(request)
        return func(request, *args, **kwargs)
    return wrapper


def tacking_request(request):
    update_total_visit_number()
    update_daily_visit_number()
    update_user_visit(request)


def update_total_visit_number():
    count_nums = TotalVisitNum.objects.all().count()
    if count_nums:
        count_nums = TotalVisitNum.objects.all()[0]
        count_nums.count = F('count') + 1
    else:
        count_nums = TotalVisitNum()
        count_nums.count = 1
    count_nums.save()


def update_user_visit(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取 ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的 ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理 ip
    UserVisit.objects.create(ip_address=client_ip, end_point=request.path)


def update_daily_visit_number():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    today = DailyVisitNum.objects.filter(day=date)
    if today:
        today = today[0]
        today.count += 1
    else:
        today = DailyVisitNum()
        today.dayTime = date
        today.count = 1
    today.save()
