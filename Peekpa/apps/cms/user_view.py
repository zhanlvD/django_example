from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from apps.bloguser.models import User
from apps.cms.forms import UserAddForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.bloguser.decorators import peekpa_login_superuser_required


@method_decorator(login_required, name='post')
@method_decorator(peekpa_login_superuser_required, name='post')
class UserView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = UserAddForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                User.objects.create_staffuser(email=email, username=username, password=password)
                return redirect(reverse("cms:user_manage_view"))
            else:
                return redirect(reverse("cms:user_publish_view"))
        # 修改Tag
        elif 'modify' in request.POST:
            form = UserEditForm(request.POST)
            if form.is_valid():
                uid = form.cleaned_data.get('pk')
                password = form.cleaned_data.get('password')
                user = User.objects.get(uid=uid)
                user.set_password(password)
                user.save()
                return redirect(reverse("cms:user_manage_view"))
            else:
                return redirect(reverse("cms:user_manage_view"))
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:user_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:user_publish_view"))


@method_decorator(login_required, name='get')
@method_decorator(peekpa_login_superuser_required, name='get')
class UserEditView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        post = User.objects.get(uid=user_id)
        context = {
            'item_data': post,
        }
        return render(request, 'cms/user/publish.html', context=context)


@method_decorator(login_required, name='get')
@method_decorator(peekpa_login_superuser_required, name='get')
class UserDeleteView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.get(uid=user_id)
        user.is_active = False
        user.save()
        return redirect(reverse("cms:user_manage_view"))