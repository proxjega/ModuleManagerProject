from django.shortcuts import redirect, render
from django.http import HttpResponse

from . import forms
from . import services

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register(request):
    pass

def module_create(request):
    if request.method == "POST":
        form = forms.ModuleForm(request.POST)
        if form.is_valid():
            services.create_module(request.user, form.cleaned_data)
            return redirect("modules")
    else:
        form = forms.ModuleForm()
    return render()