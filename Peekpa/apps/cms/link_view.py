import markdown
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from apps.bloguser.models import User
from apps.cms.forms import LinkAddForm, LinkEditForm
from apps.link.models import Link
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='post')
class LinkView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = LinkAddForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                show_name = form.cleaned_data.get('show_name')
                url = form.cleaned_data.get('url')
                status = form.cleaned_data.get('status')
                Link.objects.create(name=name, show_name=show_name, url=url, status=status)
                return redirect(reverse("cms:link_manage_view"))
            else:
                return redirect(reverse("cms:link_publish_view"))
        # 修改Link
        elif 'modify' in request.POST:
            form = LinkEditForm(request.POST)
            if form.is_valid():
                pk = form.cleaned_data.get('pk')
                name = form.cleaned_data.get('name')
                show_name = form.cleaned_data.get('show_name')
                url = form.cleaned_data.get('url')
                status = form.cleaned_data.get('status')
                instance = Link.objects.filter(id=pk)
                instance.update(name=name, show_name=show_name, url=url, status=status)
                return redirect(reverse("cms:link_manage_view"))
            else:
                return redirect(reverse("cms:link_manage_view"))
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:link_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:link_publish_view"))


@method_decorator(login_required, name='get')
class LinkEditView(View):
    def get(self, request):
        link_id = request.GET.get('link_id')
        link = Link.objects.get(pk=link_id)
        context = {
            'item_data': link,
            'list_data_status': Link.STATUS_ITEMS,
        }
        return render(request, 'cms/link/publish.html', context=context)


@method_decorator(login_required, name='get')
class LinkDeleteView(View):
    def get(self, request):
        link_id = request.GET.get('link_id')
        Link.objects.filter(id=link_id).update(status=Link.STATUS_DELETE)
        return redirect(reverse("cms:link_manage_view"))

