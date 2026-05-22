from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("successful-registration/", views.successful_registration, name="successful-registration"),
    path("profile/", views.profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("module_create/", views.module_create, name="module_create"),
    path("modules/", views.modules, name="modules"),
    path("modules/<int:module_id>/", views.module_info, name="module_info"),
    path("modules/<int:module_id>/delete/", views.module_delete, name="module_delete"),
    path("modules/<int:module_id>/pdf/", views.module_pdf, name="module_pdf"),
]