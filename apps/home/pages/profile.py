from django. contrib. auth. models import User
from django.shortcuts import redirect
from posixpath import split
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from ..views import get_default_page_context

from django import forms
from django.contrib.auth.models import User


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))


@login_required(login_url="/login/")
def profileIndex(request):
    success = True
    msg = ""
    form = PasswordChangeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if password1 == password2:
                request.user.set_password(password1)
                request.user.save()
                success = True
                msg = "Password was changed successfully"
            else:
                success = False
                msg = "Password is not matched"
        else:
            success = False

    context = {
        "form": form,
        "success": success,
        "msg": msg
    }
    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render({**get_default_page_context(request), **context}, request))
