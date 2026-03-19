from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from . import forms
from . import services

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            services.register_user(form.cleaned_data)
            return redirect("successful-registration") #do this
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