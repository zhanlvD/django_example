# encoding: utf-8
from django.shortcuts import redirect, reverse


def peekpa_login_superuser_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        return redirect(reverse('cms:login'))
    return wrapper
