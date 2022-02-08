from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from accounts.forms import LoginForm, RegisterForm
from django.conf import settings
from accounts.models import Users
from django.http import HttpResponseRedirect
from django.urls import reverse


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = Users.objects.create_user(account = email, username=username, email = email, password = password)
        except:
            user = None
        if user != None:
            login(request, user)
            return redirect("/login/")
        else:
            request.session['register_error'] = 1 # 1 == True
    return render(request, "register.html", {"form": form})


def login_view(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect("/home/")
        else:
            print("login Fail!")
    return render(request, "login.html", {'login_form': login_form})