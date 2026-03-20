from django.shortcuts import redirect, render
from django.http import HttpResponse

from . import forms
from . import services

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register(request):
    form = forms.RegisterForm()
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            services.register_user(form.cleaned_data)
            return HttpResponse("Good") #do this redirect("successful-registration")
    return render(request, "registration/register.html", {"form":form}) # template

def module_create(request):
    if request.method == "POST":
        form = forms.ModuleForm(request.POST)
        if form.is_valid():
            services.create_module(request.user, form.cleaned_data)
            return redirect("modules") #do this
    else:
        form = forms.ModuleForm()
    return render() # template


def profile(request):
    if request.user.is_authenticated == False:
        return redirect("login")
    return render(request, "accounts/profile.html")