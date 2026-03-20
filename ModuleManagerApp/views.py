from django.shortcuts import redirect, render
from django.http import HttpResponse

from . import forms
from . import services

def index(request):
    return render(request, "index.html")

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
    return render(request, "module_create") # template


def profile(request):
    if request.user.is_authenticated == False:
        return redirect("login")
    if request.method == "POST":
        form = forms.ProfileEditForm(request.POST)
        if form.is_valid():
            services.redact_profile(request.user, form.cleaned_data)
            return redirect("profile")
    else:
        is_edit_mode = request.GET.get("edit") == "1"
        if is_edit_mode:
            form = forms.ProfileEditForm(instance=request.user)
            return render(request, "accounts/profile.html", {"form":form})
    return render(request, "accounts/profile.html")