from django.contrib import admin

from .models import Module, CustomUser

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'delivery_mode', 'credits', 'user']
    list_filter = ['module_type', 'delivery_mode', 'language']
    search_fields = ['title', 'teacher']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'degree', 'study_institution', 'name_of_program']
    list_filter = ['degree', 'study_institution']
    search_fields = ['username', 'email']
