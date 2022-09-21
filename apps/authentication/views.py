# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from apps.home.models import AllowRegister


def canRegister():
    allows = AllowRegister.objects.all()
    if len(allows) > 0:
        if allows[0].Status == "on":
            return True
        else:
            return False
    else:
        return True


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            capatchacode = form.cleaned_data.get("capatchacode")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    register_on = False
    if canRegister():
        register_on = True
    msg = None
    success = False

    if request.method == "POST":
        if canRegister():
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                success = True
            else:
                msg = 'Form is not valid'
        else:
            form = SignUpForm()
            msg = "User registeration is not allowed"
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success, "register_on": register_on})
